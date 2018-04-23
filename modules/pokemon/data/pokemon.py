from Move import Move
from math import floor
from math import ceil


class Pokemon(object):
    POKEDEX = {}
    CPMUL = {}

    def __init__(self, name, level, atk_iv, def_iv, sta_iv, fast):
        self.name = name
        self.level = level
        pokemon_stat = []
        if len(Pokemon.POKEDEX) == 0:
            f = open("Pokedex.csv", 'r')
            for entry in f:
                entry = entry.strip()
                pokeList = entry.split(",")
                Pokemon.POKEDEX[pokeList[0]] = pokeList
            f.close()
        for key in Pokemon.POKEDEX:
            if key.lower() == self.name.lower():
                pokemon_stat = Pokemon.POKEDEX[key]
        self.cpm = 0
        if len(Pokemon.CPMUL) == 0:
            f = open("CP_multiplier.csv", 'r')
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
              "\nType2: " + str(self.type2) + "\nATK: " + str(self.attack) + \
              "\nDEF: " + str(self.defense) + "\nSTA: " + \
              str(self.stamina) + "\nFast Move:" + str(self.fast)
        return msg

    def fast_move_dmg(self, pokemon):
        if self.fast.type in [self.type1, self.type2]:
            STAB = 1.2
        else:
            STAB = 1.0
        f = open("Type_advantages.csv", 'r')
        typeDic = {}
        for line in f:
            line = line.strip()
            typeList = line.split(",")
            typeDic[typeList[0]] = typeList
        f.close()

        Effective = 1.0
        for key in typeDic:
            if typeDic[key][1] == self.fast.type and \
               typeDic[key][2] == pokemon.type1:
                Effective *= float(typeDic[key][3])
            if typeDic[key][1] == self.fast.type and \
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
        f = open("Type_advantages.csv", 'r')
        typeDic = {}
        for line in f:
            line = line.strip()
            typeList = line.split(",")
            typeDic[typeList[0]] = typeList
        f.close()
        Effective = 1.0
        for key in typeDic:
            if typeDic[key][1] == self.charge.type and \
               typeDic[key][2] == pokemon.type1:
                Effective *= float(typeDic[key][3])
            if typeDic[key][1] == self.charge.type and \
               typeDic[key][2] == pokemon.type2:
                Effective *= float(typeDic[key][3])
        dmg = floor(0.5 * self.charge.power * (
                    (self.attack * self.cpm) / (
                        pokemon.defense * pokemon.cpm)) *
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
