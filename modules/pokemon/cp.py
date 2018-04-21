from ..i_module import IModule, ExecResp
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
import math
import re
import json
from fuzzywuzzy import fuzz


class CpModule(IModule):

    __POKEMON_REGEX = "[\.a-zA-Z\'\-]+"

    __WILD_CP_LIMIT = 35

    __LVL_MULTIPLIER = [
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
        self.__common_pokemons = self._get_common_pokemons()
        # BotLogger().debug(self.__pokemon_stats)
        # BotLogger().debug(self.__common_pokemons)
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

    def _get_common_pokemons(self):
        # returns a dictionary where the pokemon name is the key
        # the value is another dictionary, with key "atk", "def", "sta"
        file = "./modules/pokemon/weather_cps.json"
        commons = {}
        with open(file, "r") as fp:
            commons = json.loads(fp.read())
        return commons

    def _compute_cp(self, level,
                    base_atk, base_def, base_sta,
                    iv_atk=15, iv_def=15, iv_sta=15):
            m = self.__LVL_MULTIPLIER[level - 1]
            atk = (base_atk + iv_atk) * m
            defen = (base_def + iv_def) * m
            sta = (base_sta + iv_sta) * m
            cp = max(10, math.floor(math.sqrt(atk * atk * defen * sta) / 10))
            return cp

    def _compute_cps(self, pokemon, iv_atk=15, iv_def=15, iv_sta=15):
        pokemon_stat = self.__pokemon_stats[pokemon]
        base_atk = pokemon_stat["atk"]
        base_def = pokemon_stat["def"]
        base_sta = pokemon_stat["sta"]
        out = {}
        for lvl in range(1, self.__WILD_CP_LIMIT+1):
            out[lvl] = self._compute_cp(lvl, base_atk, base_def, base_sta,
                                        iv_atk, iv_def, iv_sta)
        return out

    def _compute_hp(self, level, base_sta, iv_sta=15):
            m = self.__LVL_MULTIPLIER[level - 1]
            sta = (base_sta + iv_sta) * m
            hp = max(10, math.floor(sta))
            return hp

    def _compute_hps(self, pokemon, iv_sta=15):
        pokemon_stat = self.__pokemon_stats[pokemon]
        base_sta = pokemon_stat["sta"]
        out = {}
        for lvl in range(1, self.__WILD_CP_LIMIT+1):
            out[lvl] = self._compute_hp(lvl, base_sta, iv_sta)
        return out

    # """
    # Main Execute Function
    # """
    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        command = cmd_args[0]

        # """
        # command: cp
        if command == "cp":
            if not re.match("^cp( {})+$".format(self.__POKEMON_REGEX), cmd):
                msg = "Usage: {}cp poke1 poke2 ...".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            queried_pokemons = [poke.lower() for poke in cmd_args[1:]]
            for poke in queried_pokemons:
                if poke not in self.__pokemon_stats:
                    msg = "{} is not a pokemon.".format(poke)
                    embed = EmbedHelper.error(msg)
                    return [ExecResp(code=500, args=embed)]

            return self.__handle_cp(queried_pokemons)

        # """
        # command: cpstr
        if command == "cpstr":
            if not re.match("^cpstr( {})+$".format(self.__POKEMON_REGEX), cmd):
                msg = "Usage: {}cpstr poke1 poke2 ...".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            queried_pokemons = [poke.lower() for poke in cmd_args[1:]]
            guess_lst = []
            for poke in queried_pokemons:
                ratio = {}
                for name in self.__pokemon_stats:
                    r = fuzz.ratio(poke, name)
                    ratio[name] = r
                guess_lst.append(max(ratio, key=lambda k: ratio[k]))
            queried_pokemons = guess_lst

            return self.__handle_cpstr(queried_pokemons)

        # """
        # command: cpstrw
        if command == "cpstrw":
            weathers = self.__common_pokemons["weather"].keys()
            weathers_str = "|".join(weathers)
            if not re.match("^cpstrw ({})$".format(weathers_str), cmd):
                msg = "Usage: {}cpstrw [{}]".format(
                      BotConfig().get_botprefix(),
                      weathers_str)
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            weather = cmd_args[1]
            return self.__handle_cpstrw(weather)

        # """
        # command: cpstrc
        if command == "cpstrc":
            if not re.match("^cpstrc$", cmd):
                msg = "Usage: {}cpstrc".format(BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            return self.__handle_cpstrc()

        # not handled by this module
        return None

    # """
    # command handler: cp
    # """
    def __handle_cp(self, queried_pokemons):
        ret_list = []
        for poke in queried_pokemons:
            cps = self._compute_cps(poke)
            cps = list(sorted(cps.values(), reverse=True))

            embed = EmbedHelper.success()
            embed.title = "Max CP for {}".format(poke)
            i = 0
            while i < len(cps):
                lvl = len(cps)-i
                if i == 0:
                    value_format = "`{}{:>5}{:>5}{:>5}{:>5}`"
                    values = cps[i:i+5]
                    embed.add_field(
                        name="LV{} to {}:".format(lvl, lvl-4),
                        value=value_format.format(*values),
                        inline=False)
                    i = i+5
                else:
                    value_format = "`\n{}{:>5}{:>5}{:>5}{:>5}`\n"\
                                   "`{}{:>5}{:>5}{:>5}{:>5}`"
                    values = cps[i:i+10]
                    embed.add_field(
                        name="LV{} to {}:".format(lvl, lvl-9),
                        value=value_format.format(*values),
                        inline=False)
                    i = i+10
            ret_list.append(ExecResp(code=200, args=embed))
        # end for
        return ret_list

    # """
    # command handler: cpstr
    # """
    def __handle_cpstr(self, queried_pokemons):
        all_cps = set()
        for poke in queried_pokemons:
            cps = self._compute_cps(poke)
            for cp in list(cps.values()):
                all_cps.add(cp)

        # correction for nidorans
        for i in range(len(queried_pokemons)):
            if queried_pokemons[i] == "nidoranm":
                queried_pokemons[i] = "nidoran\u2642"
            if queried_pokemons[i] == "nidoranf":
                queried_pokemons[i] = "nidoran\u2640"

        all_poke = ','.join(queried_pokemons)
        sorted_cps = sorted(all_cps, reverse=True)
        all_cps = ','.join(["cp"+str(cp) for cp in sorted_cps])
        str_out = all_poke + '&' + all_cps

        if len(queried_pokemons) > 1:
            poke_out = ','.join(queried_pokemons)
            return [ExecResp(code=210, args=str_out),
                    ExecResp(code=210, args=poke_out)]
        else:
            return [ExecResp(code=210, args=str_out)]

    # """
    # command handler: cpstrw
    # """
    def __handle_cpstrw(self, weather):
        weather_mons = self.__common_pokemons["weather"][weather]
        weather_mons = [poke.lower() for poke in weather_mons]
        return self.__handle_cpstr(weather_mons)

    # """
    # command handler: cpstrc
    # """
    def __handle_cpstrc(self):
        common_mons = self.__common_pokemons["commons"]
        common_mons = [poke.lower() for poke in common_mons]
        return self.__handle_cpstr(common_mons)
