from ..i_module import IModule, ExecResp
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
import math
import re
from discord import Embed


class CpModule(IModule):

    __POKEMON_REGEX = "[\-\.a-zA-Z]+"

    __CP_MULTIPLIER = [
        0.094, 0.16639787, 0.21573247, 0.25572005, 0.29024988,
        0.3210876, 0.34921268, 0.37523559, 0.39956728, 0.42250001,
        0.44310755, 0.46279839, 0.48168495, 0.49985844, 0.51739395,
        0.53435433, 0.55079269, 0.56675452, 0.58227891, 0.59740001,
        0.61215729, 0.62656713, 0.64065295, 0.65443563, 0.667934,
        0.68116492, 0.69414365, 0.70688421, 0.71939909, 0.7317,
        0.73776948, 0.74378943, 0.74976104, 0.75568551, 0.76156384,
        0.76739717, 0.7731865, 0.77893275, 0.78463697, 0.79030001]

    def __init__(self):
        self.__pokemon_stats = self._get_pokemon_stats()
        # BotLogger().debug(self.__pokemon_stats)
        return

    def _get_pokemon_stats(self):
        # returns a dictionary where the pokemon name is the key
        # the value is another dictionary, with key "atk", "def", "sta"
        file = "./modules/pokemon/stats"
        stats = {}
        with open(file) as fp:
            lines = fp.read().splitlines()
            for line in lines:
                line_items = line.split()
                poke = line_items[0].lower()
                stats[poke] = {}
                stats[poke]["atk"] = int(line_items[1])
                stats[poke]["def"] = int(line_items[2])
                stats[poke]["sta"] = int(line_items[3])
        return stats

    def _compute_cp(self, level,
                    base_atk, base_def, base_sta,
                    iv_atk=15, iv_def=15, iv_sta=15):
            m = self.__CP_MULTIPLIER[level - 1]
            atk = (base_atk + iv_atk) * m
            defen = (base_def + iv_def) * m
            sta = (base_sta + iv_sta) * m
            cp = int(max(10, math.floor(math.sqrt(
                atk * atk * defen * sta) / 10)))
            return cp

    def _compute_cps(self, pokemon, iv_atk=15, iv_def=15, iv_sta=15):
        pokemon_stat = self.__pokemon_stats[pokemon]
        base_atk = pokemon_stat["atk"]
        base_def = pokemon_stat["def"]
        base_sta = pokemon_stat["sta"]
        out = {}
        for lvl in range(1, 31):
            out[lvl] = self._compute_cp(lvl, base_atk, base_def, base_sta,
                                        iv_atk, iv_def, iv_sta)
        return out

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        command = cmd_args[0]

        # """
        # command: cp
        # """
        if command == "cp":
            # BotLogger().debug("CP")
            if not re.match("cp( {})+$".format(self.__POKEMON_REGEX), cmd):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}cp poke1 poke2 ...".format(
                                    BotConfig().get_botprefix())
                return [ExecResp(code=500, args=embed)]

            queried_pokemons = [poke.lower() for poke in cmd_args[1:]]
            for poke in queried_pokemons:
                if poke not in self.__pokemon_stats:
                    embed = Embed()
                    embed.colour = BotConfig().get_hex("Colors", "OnError")
                    embed.description = "{} is not a pokemon.".format(poke)
                    return [ExecResp(code=500, args=embed)]

            ret_list = []
            for poke in queried_pokemons:
                cps = self._compute_cps(poke)

                embed = Embed()
                embed.title = "Max CP for {}".format(poke)
                embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
                for i in range(30, 0, -10):
                    field_format = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}"
                    embed.add_field(name="LV{} to {}:".format(i, i - 9),
                                    value=field_format.format(
                                    cps[i], cps[i - 1], cps[i - 2], cps[i - 3],
                                    cps[i - 4], cps[i - 5], cps[i - 6],
                                    cps[i - 7], cps[i - 8], cps[i - 9]),
                                    inline=True)
                ret_list.append(ExecResp(code=200, args=embed))
            return ret_list

        # """
        # command: cpstr
        # """
        if command == "cpstr":
            if not re.match("cpstr( {})+$".format(self.__POKEMON_REGEX), cmd):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}cpstr poke1 poke2 ...".format(
                                    BotConfig().get_botprefix())
                return [ExecResp(code=500, args=embed)]

            queried_pokemons = [poke.lower() for poke in cmd_args[1:]]
            for poke in queried_pokemons:
                if poke not in self.__pokemon_stats:
                    embed = Embed()
                    embed.colour = BotConfig().get_hex("Colors", "OnError")
                    embed.description = "{} is not a pokemon.".format(poke)
                    return [ExecResp(code=500, args=embed)]

            all_cps = set()
            for poke in queried_pokemons:
                cps = self._compute_cps(poke)
                for cp in list(cps.values()):
                    all_cps.add(cp)

            all_poke = ",".join(queried_pokemons) + '&'
            sorted_cps = sorted(all_cps, reverse=True)
            all_cps = ",".join(["cp"+str(cp) for cp in sorted_cps])
            str_out = all_poke + all_cps
            return [ExecResp(code=210, args=str_out)]

        # not handled by this module
        return None
