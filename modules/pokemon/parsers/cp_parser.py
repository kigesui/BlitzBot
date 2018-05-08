from . import ArgParser, ArgParserException
from . import ParserException
from . import IVParser
from .pokemon_parser import PokemonParser

import re


class PrivateParser():
    """ private class """
    def __init__(self, prog, init_lists=None):
        self.__lists = init_lists
        self.__poke_parser = PokemonParser()
        self.parser = ArgParser(prog=prog, add_help=False)
        self.parser.add_argument("poke", nargs="*", type=str,
                                 help="Name of the query Pokemons")
        self.parser.add_argument("-l", "--list", type=str,
                                 help="Add pre-defined Pokemon lists []")
        self.parser.add_argument("-iv", type=str, default="fff",
                                 help="Specify IV(s) [default is fff]")
        self.parser.add_argument("-h", "--help", action='store_true',
                                 help="Print help.")
        return

    def parse_args(self, args):
        args = re.findall(r'(-{0,2}\w+|".*?")', args)
        pokelist = []
        iv_set = None
        try:
            args = self.parser.parse_args(args)

            if args.help:
                raise ParserException(self.parser.format_help())

            # get set of pokemon
            for poke in args.poke:
                poke = poke.replace("\"", "")
                if poke not in pokelist:
                    pokelist.append(poke)

            # get pre-defined list
            if args.list:
                pokes = self._get_pokemons_from_lists(args.list)
                for poke in pokes:
                    if poke not in pokelist:
                        pokelist.append(poke)

            # get set of ivs
            if args.iv:
                iv_set = IVParser().parse_str(args.iv)

        except ArgParserException:
            raise ParserException(self.parser.format_usage())
        # call pokemon parser to get pokemon numbers from name
        pokenumbers = []
        for poke in pokelist:
            pokenumbers.append(self.__poke_parser.parse_name(poke))
            # raise ParserException("{} is not a pokemon".format(poke))
        return pokenumbers, iv_set, args

    def _get_pokemons_from_lists(self, pokelist_str):
        if not self.__lists:
            raise ParserException("There are no lists.")
        pokelists = re.findall(r'(\w+)', pokelist_str)
        pokes = []
        for l in pokelists:
            if l not in self.__lists.keys():
                lists = self.__lists.keys()
                lists_str = "|".join(lists)
                raise ParserException(
                    "{} is not a valid list. ".format(l) +
                    "Valid lists are [{}]".format(lists_str))
            pokes += self.__lists[l]
        return pokes


class CpParser:
    """ public class """

    """ singleton """
    instance = None

    """ public methods """
    def __init__(self, init_lists=None):
        if not CpParser.instance:
            CpParser.instance = PrivateParser("cp", init_lists)

    def parse_args(self, args):
        pokemon_numbers, iv_set, _ = CpParser.instance.parse_args(args)
        return pokemon_numbers, iv_set


class CpStrParser:
    """ public class """

    """ singleton """
    instance = None

    """ public methods """
    def __init__(self, init_lists=None):
        if not CpStrParser.instance:
            CpStrParser.instance = PrivateParser("cpstr", init_lists)
            CpStrParser.instance.parser.add_argument(
                "-b", "--breaks", type=int, default=5,
                help="Break after certain number.")

    def parse_args(self, args):
        # return list of numbers
        pokemon_numbers, iv_set, args = CpStrParser.instance.parse_args(args)
        break_len = args.breaks
        if break_len < 1:
            raise ParserException("-b needs to be a positive integer.")
        return pokemon_numbers, iv_set, break_len
