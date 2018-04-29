from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
from fuzzywuzzy import fuzz
from numpy import arange
from math import floor
from math import ceil


class BreakPointModule(IModule):
    __BOSS_LVL = {1: 20,
                  2: 25,
                  3: 30,
                  4: 40,
                  5: 50}
    __BOSS_HP = {1: 600,
                 2: 1800,
                 3: 3000,
                 4: 7500,
                 5: 12500}
    ak = 15
    df = 15
    hp = 15

    def __init__(self):
        return

    def cal_bp(self, attack_mon, atk_move,
               boss_mon, tier, boss_move):
        boss = Pokemon(boss_mon, self.__BOSS_LVL[tier],
                       15, 15, self.__BOSS_HP[tier], boss_move)
        dmg_bp = {}
        def_bp = {}
        dmg = {}
        hurt = {}
        for lvl in arange(30, 40.5, 0.5):
            attacker = Pokemon(attack_mon, lvl,
                               self.ak, self.df, self.hp, atk_move)
            atk_dmg = attacker.fast_move_dmg(boss)
            boss_dmg = boss.fast_move_dmg(attacker)
            dmg[lvl] = atk_dmg
            hurt[lvl] = boss_dmg
            if lvl > 30:
                if dmg[lvl] > dmg[lvl - 0.5]:
                    dmg_bp[lvl] = atk_dmg
                else:
                    pass
                if hurt[lvl] < hurt[lvl - 0.5]:
                    def_bp[lvl] = boss_dmg
            else:
                pass
        return attacker.name, boss.name, attacker.fast.name, \
            boss.fast.name, dmg_bp, def_bp

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(',')
        command = cmd_args[0].strip()
        if command == "bp":
            # if len(kwargs) > 0:
            #     for k, v in kwargs.itmes():
            #         if hasattr(self, k):
            #             setattr(self, k, v)
            attack_mon, atk_move, boss_mon, tier, boss_move = \
                cmd_args[1].strip(), cmd_args[2].strip(), cmd_args[3].strip(),\
                int(cmd_args[4].strip()), cmd_args[5].strip()
            attacker_name, boss_name, a_move_name, b_move_name, dmg_bp, def_bp\
                = self.cal_bp(attack_mon, atk_move, boss_mon, tier, boss_move)
            embed = EmbedHelper.success()
            embed.title = "Breakpoint(s) for {} (15 atk, 15 def) against {}"\
                          .format(attacker_name, boss_name)
            if len(dmg_bp) > 0:
                dmg_str = '\n'.join('LV ' + str(k) + ': ' + str(v) for k, v in dmg_bp.items())
            else:
                dmg_str = '{} doesn\'t have any damage breakpoint above\
                level 30.'.format(attacker_name)
            if len(def_bp) > 0:
                def_str = '\n'.join('LV ' + str(k) + ': ' + str(v) for k, v in def_bp.items())
            else:
                def_str = '{} doesn\'t have any defense breakpoint above\
                level 30.'.format(attacker_name)
            embed.add_field(name='Damage breakpoint of {}'.format(a_move_name),
                            value=dmg_str,
                            inline=False)
            embed.add_field(name='Defense breakpoint for {}'
                            .format(b_move_name),
                            value=def_str,
                            inline=False)
            return [ExecResp(code=200, args=embed)]
        # not handled by this module
        return None


class Move(object):
    MOVES = {}

    def __init__(self, name):
        self.name = name
        move_info = []
        if len(Move.MOVES) == 0:
            f = open("./modules/pokemon/Pokemon_moves.csv", 'r')
            for move in f:
                move = move.strip()
                moveList = move.split(",")
                Move.MOVES[moveList[0]] = moveList
            f.close()

        guess_lst = {}
        for key in Move.MOVES:
            r = fuzz.ratio(key.lower(), self.name.lower())
            guess_lst[key] = r
        move_info = Move.MOVES[max(guess_lst, key=lambda k: guess_lst[k])]
        self.name = move_info[0]
        if len(move_info) == 0:
            print('I can\'t recognize' + ' ' + self.name)
            return

        self.type = move_info[1]  # Move type
        self.power = int(move_info[2])

        # For in-battle calculations
        self.duration = float(move_info[3])  # Move's base damage
        self.energy = int(move_info[4])

    def __str__(self):
        msg = self.name + '\nType:' + self.type + '\nPower:' + str(self.power)\
            + '\nDuration:' + str(self.duration)\
            + '\nEnergy:' + str(self.energy)

        return msg


class Pokemon(object):
    POKEDEX = {}
    CPMUL = {}

    def __init__(self, name, level, atk_iv, def_iv, sta_iv, fast):
        self.name = name
        self.level = level
        pokemon_stat = []
        if len(Pokemon.POKEDEX) == 0:
            f = open("./modules/pokemon/Pokedex.csv", 'r')
            for entry in f:
                entry = entry.strip()
                pokeList = entry.split(",")
                Pokemon.POKEDEX[pokeList[0]] = pokeList
            f.close()
        guess_lst = {}
        for key in Pokemon.POKEDEX:
            r = fuzz.ratio(key.lower(), self.name.lower())
            guess_lst[key] = r
        pokemon_stat = Pokemon.POKEDEX[max(
            guess_lst, key=lambda k: guess_lst[k])]
        self.name = pokemon_stat[0]
        self.cpm = 0
        if len(Pokemon.CPMUL) == 0:
            f = open("./modules/pokemon/CP_multiplier.csv", 'r')
            for entry in f:
                entry = entry.strip()
                cpmList = entry.split(",")
                Pokemon.CPMUL[cpmList[0]] = cpmList
            f.close()
        for key in Pokemon.CPMUL:
            if float(key) == float(self.level):
                self.cpm = float(Pokemon.CPMUL[key][1])
        self.type1 = pokemon_stat[1]
        self.type2 = pokemon_stat[2]
        self.attack = int(pokemon_stat[3]) + atk_iv
        self.defense = int(pokemon_stat[4]) + def_iv
        if sta_iv < 16:
            self.stamina = int(pokemon_stat[5]) + sta_iv
        else:
            self.stamina = int(sta_iv)
        self.fast = Move(fast)
        self.energy = 0

    def __str__(self):
        msg = "Name: " + str(self.name) + "\nType1: " + str(self.type1) + \
              "\nType2: " + str(self.type2) + "\nATK: " + str(self.attack)\
              + "\nDEF: " + str(self.defense) + "\nSTA: " + \
              str(self.stamina) + "\nFast Move:" + str(self.fast)
        return msg

    def fast_move_dmg(self, pokemon):
        if self.fast.type in [self.type1, self.type2]:
            STAB = 1.2
        else:
            STAB = 1.0
        f = open("./modules/pokemon/Type_advantages.csv", 'r')
        typeDic = {}
        for line in f:
            line = line.strip()
            typeList = line.split(",")
            typeDic[typeList[0]] = typeList
        f.close()

        Effective = 1.0
        for key in typeDic:
            if typeDic[key][1] == self.fast.type and\
               typeDic[key][2] == pokemon.type1:
                Effective *= float(typeDic[key][3])
            if typeDic[key][1] == self.fast.type and\
               typeDic[key][2] == pokemon.type2:
                Effective *= float(typeDic[key][3])
        dmg = floor(0.5 * self.fast.power * (
                    (self.attack * self.cpm) / (
                        pokemon.defense * pokemon.cpm)) *
                    STAB * Effective) + 1
        return dmg

    def charge_move_dmg(self, pokemon):
        if self.charge.type in [self.type1, self.type2]:
            STAB = 1.2
        else:
            STAB = 1.0
        f = open("./modules/pokemon/Type_advantages.csv", 'r')
        typeDic = {}
        for line in f:
            line = line.strip()
            typeList = line.split(",")
            typeDic[typeList[0]] = typeList
        f.close()
        Effective = 1.0
        for key in typeDic:
            if typeDic[key][1] == self.charge.type and typeDic[key][2] == pokemon.type1:
                Effective *= float(typeDic[key][3])
            if typeDic[key][1] == self.charge.type and typeDic[key][2] == pokemon.type2:
                Effective *= float(typeDic[key][3])
        dmg = floor(0.5 * self.charge.power * (
                    (self.attack * self.cpm) / (pokemon.defense * pokemon.cpm)) *
                    STAB * Effective) + 1
        return dmg

    def uses_fast_move_on(self, pokemon, dmg):
        self.energy += self.fast.energy
        pokemon.stamina -= dmg
        if pokemon.stamina <= 0:
            return 0
        pokemon.energy += ceil(dmg / 2)
        if pokemon.energy > 100:
            pokemon.energy = 100
        return pokemon.stamina

    def uses_charge_move_on(self, pokemon, dmg):
        self.energy -= self.charge.energy
        pokemon.stamina -= dmg
        if pokemon.stamina <= 0:
            return 0
        pokemon.energy += ceil(dmg / 2)
        if pokemon.energy > 100:
            pokemon.energy = 100
        return pokemon.stamina
