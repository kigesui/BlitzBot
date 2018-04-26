from . import ArgParser, ArgParserException
from . import ParserException
from .pokemon_parser import PokemonParser

import re


class PrivateParser():
    """ private class """
    def __init__(self, prog, init_lists=None):
        self.__lists = init_lists
        self.__poke_parser = PokemonParser()
        self.parser = ArgParser(prog=prog, add_help=False)
        self.parser.add_argument("poke", nargs="*", type=str,
                                 help="poke1 poke2 ...")
        self.parser.add_argument("-l", "--list", type=str,
                                 help="Add pre-defined Pokemon lists []")
        return

    def parse_args(self, args):
        args = re.findall(r'(-{0,2}\w+|".*?")', args)
        pokelist = []
        try:
            args = self.parser.parse_args(args)
            for poke in args.poke:
                poke = poke.replace("\"", "")
                if poke not in pokelist:
                    pokelist.append(poke)
            if args.list:
                pokes = self._get_pokemons_from_lists(args.list)
                for poke in pokes:
                    if poke not in pokelist:
                        pokelist.append(poke)
        except ArgParserException:
            raise ParserException(self.parser.format_usage())
        # call pokemon parser to get pokemon numbers from name
        pokenumbers = []
        for poke in pokelist:
            pokenumbers.append(self.__poke_parser.parse_name(poke))
            # raise ParserException("{} is not a pokemon".format(poke))
        return pokenumbers, args

    def _get_pokemons_from_lists(self, pokelist_str):
        if not self.__lists:
            raise ParserException("There are no lists")
        pokelists = re.findall(r'(\w+)', pokelist_str)
        pokes = []
        for l in pokelists:
            if l not in self.__lists.keys():
                raise ParserException("{} is not a valid list".format(l))
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
        pokemon_numbers, _ = CpParser.instance.parse_args(args)
        return pokemon_numbers


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
        pokemon_numbers, args = CpStrParser.instance.parse_args(args)
        break_len = args.breaks
        if break_len < 1:
            raise ParserException("-b needs to be a positive integer.")
        return pokemon_numbers, break_len
