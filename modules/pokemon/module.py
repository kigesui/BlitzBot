from ..i_module import IModule, ExecResp

# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
from .data import Pokedex, PokemonStats
from .parsers import CpParser, CpStrParser
from .parsers import ParserException

# import json
# from fuzzywuzzy import fuzz
import json
import os


class PokemonModule(IModule):

    LAZY_FILE_PATH = \
        os.path.dirname(os.path.realpath(__file__)) \
        + "/data/lazy.json"

    def __init__(self):
        lazy_dict = self._get_lazy_dict()
        self.__cp_parser = CpParser(lazy_dict)
        self.__cpstr_parser = CpStrParser(lazy_dict)
        return

    def _get_lazy_dict(self):
        lazy_dict = {}
        with open(PokemonModule.LAZY_FILE_PATH, "r") as fp:
            lazy_dict = json.loads(fp.read())
        return lazy_dict

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]

        # """
        # command: cp
        if command == "cp":
            if len(cmd_args) < 2:
                msg = "Usage: {}cp poke1 poke2 ...".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]
            args = " ".join(cmd_args[1:])
            try:
                pokemon_numbers = self.__cp_parser.parse_args(args)
                return self.__handle_cp(pokemon_numbers)
            except ParserException as e:
                embed = EmbedHelper.error(str(e))
                return [ExecResp(code=500, args=embed)]

        # """
        # command: cpstr
        if command == "cpstr":
            if len(cmd_args) < 2:
                msg = "Usage: {}cpstr poke1 poke2 ...".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]
            args = " ".join(cmd_args[1:])
            try:
                pokemon_numbers, break_len = \
                    self.__cpstr_parser.parse_args(args)
                return self.__handle_cpstr(pokemon_numbers, break_len)
            except ParserException as e:
                embed = EmbedHelper.error(str(e))
                return [ExecResp(code=500, args=embed)]

        return None

    # """
    # command handler: cp
    # """
    def __handle_cp(self, pokemon_numbers):
        ret_list = []
        for number in pokemon_numbers:
            name = Pokedex().get_name_from_number(number)
            cps = PokemonStats().get_wild_pokemon_cps(number)
            cps = list(sorted(cps.values(), reverse=True))

            embed = EmbedHelper.success()
            embed.title = "Max CP for {}".format(name)
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
    def __handle_cpstr(self, pokemon_numbers, break_len):
        return self._compute_cp_resps(pokemon_numbers, break_len)

    def _compute_cp_resps(self, pokemon_numbers, num_per_block=0):
        # return these responses:
        # example: 5 pokemons and 3 per block
        #       poke1,poke2,poke3&cp1,cp2,...
        #       poke4,poke5&cp1,cp2,...
        #       poke1,poke2,poke3,poke4,poke5
        responses = []
        all_pokemon_names = []
        temp_pokes = set()
        temp_cps = set()
        counter = 0

        def add_pokecps_to_response(pokes, cps):
            pokes_str = ','.join(pokes)
            sorted_cps = sorted(cps, reverse=True)
            cps_str = ','.join(["cp"+str(cp) for cp in sorted_cps])
            responses.append(ExecResp(code=210, args=pokes_str+'&'+cps_str))
            responses.append(ExecResp(code=210, args="==v=="))

        for number in pokemon_numbers:
            counter = counter + 1
            cps = PokemonStats().get_wild_pokemon_cps(number)
            name = Pokedex().get_name_from_number(number)

            # fix some pokemon strings
            all_pokemon_names.append(name)

            # add to temporary array
            temp_pokes.add(name)
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
        if len(all_pokemon_names) > 1:
            all_pokemon_names = ','.join(all_pokemon_names)
            responses.append(ExecResp(code=210, args=all_pokemon_names))
            responses.append(ExecResp(code=210, args="====="))

        return responses
