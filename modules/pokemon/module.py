from ..i_module import IModule, ExecResp

# from utils.bot_logger import BotLogger
# from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
from .parsers import CpParser
from .parsers import ParserException
# import re
# import json
# from fuzzywuzzy import fuzz
# from modules.pokemon.pokestats import PokeStats


class PokemonModule(IModule):

    def __init__(self):
        self.__cp_parser = CpParser()
        return

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]

        # """
        # command: cp
        if command == "cp":
            args = " ".join(cmd_args)
            try:
                pokes = self.__cp_parser.parse_args(args)
                return self.__handle_cp(pokes)
            except ParserException as e:
                embed = EmbedHelper.error(e.message)
                return [ExecResp(code=500, args=embed)]

        return None

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
