from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
import re
import json
from fuzzywuzzy import fuzz
from modules.pokemon.pokestats import PokeStats


class CpModule(IModule):

    __POKEMON_REGEX = "[\.a-zA-Z\'\-]+"

    def __init__(self):
        self.__common_pokemons = self._get_common_pokemons()
        self.__pokestats = PokeStats()
        # BotLogger().debug(self.__common_pokemons)
        return

    def _get_common_pokemons(self):
        file = "./modules/pokemon/weather_cps.json"
        commons = {}
        with open(file, "r") as fp:
            commons = json.loads(fp.read())
        return commons

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
                if not self.__pokestats.contains(poke):
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
<<<<<<< Updated upstream
                ratio = {}
                for name in self.__pokemon_stats:
                    r = fuzz.ratio(poke, name)
                    ratio[name] = r
                guess_lst.append(max(ratio, key=lambda k: ratio[k]))
            queried_pokemons = guess_lst
=======
                if not self.__pokestats.contains(poke):
                    msg = "{} is not a pokemon.".format(poke)
                    embed = EmbedHelper.error(msg)
                    return [ExecResp(code=500, args=embed)]
>>>>>>> Stashed changes

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

    def _compute_cp_resps(self, pokemons, num_per_block=0):
        # return these responses:
        # example: 5 pokemons and 3 per block
        #       poke1,poke2,poke3&cp1,cp2,...
        #       poke4,poke5&cp1,cp2,...
        #       poke1,poke2,poke3,poke4,poke5
        pokemons = [poke.lower() for poke in pokemons]
        responses = []
        all_pokes_fixed = []
        temp_pokes = set()
        temp_cps = set()
        counter = 0

        def add_pokecps_to_response(pokes, cps):
            sorted_cps = sorted(cps, reverse=True)
            cps_str = ','.join(["cp"+str(cp) for cp in sorted_cps])
            pokes_str = ','.join(pokes)
            responses.append(ExecResp(code=210, args=pokes_str+'&'+cps_str))
            responses.append(ExecResp(code=210, args="==v=="))

        for poke in pokemons:
            counter = counter + 1
            cps = self.__pokestats.get_wild_poke_cps(poke)

            # fix some pokemon strings
            poke = self.__fix_poke_name(poke)
            all_pokes_fixed.append(poke)

            # add to temporary array
            temp_pokes.add(poke)
            for cp in list(cps.values()):
                temp_cps.add(cp)

            if num_per_block != 0:
                if (counter % num_per_block) == 0:
                    add_pokecps_to_response(temp_pokes, temp_cps)
                    temp_pokes = set()
                    temp_cps = set()

        # output if there are any remainings
        if temp_pokes:
            add_pokecps_to_response(temp_pokes, temp_cps)

        # add last line
        if len(all_pokes_fixed) > 1:
            fixed_pokes_str = ','.join(all_pokes_fixed)
            responses.append(ExecResp(code=210, args=fixed_pokes_str))
            responses.append(ExecResp(code=210, args="====="))

        return responses

    # """
    # command handler: cp
    # """
    def __handle_cp(self, pokemons):
        ret_list = []
        for poke in pokemons:
            cps = self.__pokestats.get_wild_poke_cps(poke)
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
    def __handle_cpstr(self, pokemons):
        return self._compute_cp_resps(pokemons, 5)

    # """
    # command handler: cpstrw
    # """
    def __handle_cpstrw(self, weather):
        weather_mons = self.__common_pokemons["weather"][weather]
        return self._compute_cp_resps(weather_mons, 4)

    # """
    # command handler: cpstrc
    # """
    def __handle_cpstrc(self):
        common_mons = self.__common_pokemons["commons"]
        return self._compute_cp_resps(common_mons, 2)

    # """
    # Helper Function
    # """
    def __fix_poke_name(self, poke):
        if poke == "nidoranm":
            poke = "nidoran\u2642"
        if poke == "nidoranf":
            poke = "nidoran\u2640"
        return poke
