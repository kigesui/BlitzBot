from ..i_module import IModule, ExecResp

from .data import Pokedex, PokemonStats
from .parsers import CpParser, CpStrParser
from .parsers import ParserException

# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper


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
                pokemon_ids, iv_set = self.__cp_parser.parse_args(args)
                return self.__handle_cp(pokemon_ids, iv_set)
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
                pokemon_ids, iv_set, break_len = \
                    self.__cpstr_parser.parse_args(args)
                return self.__handle_cpstr(pokemon_ids, iv_set, break_len)
            except ParserException as e:
                embed = EmbedHelper.error(str(e))
                return [ExecResp(code=500, args=embed)]

        return None

    # """
    # command handler: cp
    # """
    def __handle_cp(self, pokemon_ids, iv_set):
        ret_list = []
        for iv in iv_set:
            for pokemon_id in pokemon_ids:
                name = Pokedex().get_name_from_id(pokemon_id)
                cps = PokemonStats().get_wild_pokemon_cps(pokemon_id, iv)
                cps = list(sorted(cps.values(), reverse=True))

                embed = EmbedHelper.success()
                embed.title = "CP for {} with {}".format(name, iv)
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
    def __handle_cpstr(self, pokemon_ids, iv_set, break_len=0):
        responses = []
        lines = self._compute_cp_resps(pokemon_ids, iv_set, break_len)
        for l in lines:
            responses.append(ExecResp(code=210, args=l))
        return responses

    def _compute_cp_resps(self, pokemon_ids, iv_set, num_per_block=0):
        # TODO: extract this function and test it
        # return these strings:
        # example: 5 pokemons and 3 per block
        #       poke1,poke2,poke3&cp1,cp2,...
        #       poke4,poke5&cp1,cp2,...
        #       poke1,poke2,poke3,poke4,poke5
        ret_lines = []
        all_pokemon_names = []
        block_pokes = []
        block_cps = set()
        counter = 0

        def add_pokecps_to_response(pokes, cps):
            pokes_str = ','.join(pokes)
            sorted_cps = sorted(cps, reverse=True)
            cps_str = ','.join(["cp"+str(cp) for cp in sorted_cps])
            ret_lines.append(pokes_str+'&'+cps_str)
            ret_lines.append("==v==")

        for pokemon_id in pokemon_ids:
            counter = counter + 1

            # add pokemon name to all names
            name = Pokedex().get_name_from_id(pokemon_id)
            all_pokemon_names.append(name)

            # add to temporary array
            block_pokes.append(name)
            for iv in iv_set:
                cps = PokemonStats().get_wild_pokemon_cps(pokemon_id, iv)
                for cp in list(cps.values()):
                    block_cps.add(cp)

            if num_per_block != 0:
                if (counter % num_per_block) == 0:
                    add_pokecps_to_response(block_pokes, block_cps)
                    block_pokes = []
                    block_cps = set()

        # output if there are any remainings
        if len(block_pokes) > 0:
            add_pokecps_to_response(block_pokes, block_cps)

        # add last line
        if len(all_pokemon_names) > 1:
            all_pokemon_names = ','.join(all_pokemon_names)
            ret_lines.append(all_pokemon_names)
            ret_lines.append("=====")

        return ret_lines
