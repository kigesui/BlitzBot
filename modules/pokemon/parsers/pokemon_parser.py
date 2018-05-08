from . import ParserException
from putils import Singleton
from fuzzywuzzy import fuzz
from data import Pokedex


class PokemonParser(Singleton):

    def __init__(self):
        self.__reverse_dict = {}
        for k, v in Pokedex().get_dictionary().items():
            name = v["name"]
            name = name.lower()
            self.__reverse_dict[name] = k
        pass

    def parse_name(self, name):
        # in: pokemon name
        # out: pokemon number
        # raise: exception if name cannot get parsed
        name = name.lower()
        if name == "nidoranm":
            name = "nidoran\u2640"
        elif name == "nidoranf":
            name = "nidoran\u2642"
        if name in self.__reverse_dict.keys():
            return self.__reverse_dict[name]
        else:
            ratios = {}
            for n in self.__reverse_dict.keys():
                r = fuzz.ratio(n, name)
                ratios[n] = r
            guessed_name = max(ratios, key=lambda key: ratios[key])
            return self.__reverse_dict[guessed_name]
        #raise ParserException("{} is not a pokemon!".format(name))
