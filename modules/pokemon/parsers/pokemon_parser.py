# from . import ParserException
from putils import Singleton
from fuzzywuzzy import fuzz
from data import Pokedex


class PokemonParser(Singleton):

    def __init__(self):
        self.__lookup_list = Pokedex().get_dictionary().keys()
        # for k, v in Pokedex().get_dictionary().items():
        #     name = v["name"]
        #     name = name.lower()
        #     self.__reverse_dict[name] = k
        # pass

    def parse_name(self, name):
        # in: pokemon name
        # out: pokemon index
        # raise: exception if name cannot get parsed
        name = name.lower()

        # name corrections
        if name == "nidoranm":
            name = "32nidoran"
        elif name == "nidoranf":
            name = "29nidoran"
        elif name == "exeggutor":
            name = "exeggutor_normal"
        elif name == "mr. mime":
            name = "mr_mime"

        ratios = {}
        for n in self.__lookup_list:
            r = fuzz.ratio(n, name)
            ratios[n] = r
        return max(ratios, key=lambda key: ratios[key])
        #  raise ParserException("{} is not a pokemon!".format(name))
