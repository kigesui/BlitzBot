from . import ArgParser, ArgParserException
from . import ParserException
from .pokemon_parser import PokemonParser

import re


class PrivateParser():
    """ private class """
    def __init__(self, prog, init_lists=None):
        self.__lists = init_lists
        self.__poke_parser = PokemonParser()
        self.__parser = ArgParser(prog=prog, add_help=False)
        self.__parser.add_argument("poke", nargs="*", type=str,
                                   help="poke1 poke2 ...")
        self.__parser.add_argument("-l", "--list", type=str,
                                   help="Add pre-defined Pokemon lists []")
        return

    def parse_args(self, args):
        args = re.findall(r'(-{0,2}\w+|".*?")', args)
        pokelist = []
        try:
            args = self.__parser.parse_args(args)
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
            raise ParserException(self.__parser.format_usage())
        # call pokemon parser to get pokemon numbers from name
        pokenumbers = []
        for poke in pokelist:
            pokenumbers.append(self.__poke_parser.parse_name(poke))
            # raise ParserException("{} is not a pokemon".format(poke))
        return pokenumbers

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
        return CpParser.instance.parse_args(args)


class CpStrParser:
    """ public class """

    """ singleton """
    instance = None

    """ public methods """
    def __init__(self):
        if not CpStrParser.instance:
            CpStrParser.instance = PrivateParser("cpstr")

    def parse(self, command):
        return CpStrParser.instance.parse(command)
