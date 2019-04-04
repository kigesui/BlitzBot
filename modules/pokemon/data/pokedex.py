from putils import Singleton

import json
import os
import re


class Pokedex(Singleton):

    GM_FILE = "gm-0.133.0.json"

    def __init__(self):
        self.__dict = self._load_dex_from_gm()

    def get_dictionary(self):
        return dict(self.__dict)

    def get_stats_from_id(self, id):
        if id in self.__dict:
            attack = self.__dict[id]["atk"]
            defence = self.__dict[id]["def"]
            stamina = self.__dict[id]["sta"]
            return (attack, defence, stamina)
        return None

    def get_name_from_id(self, id):
        if id in self.__dict:
            return self.__dict[id]["name"]
        return None

    """ Load from Game Master """
    def _load_dex_from_gm(self):
        file = \
            os.path.dirname(os.path.realpath(__file__)) \
            + "/gamemaster/" + self.GM_FILE
        pokedex = {}
        with open(file, 'r') as fp:
            gm = json.loads(fp.read())
            self._load_stats_from_gm(pokedex, gm)
        return pokedex

    def _load_stats_from_gm(self, pokedex, gm):
        # input:
        #   - empty pokedex
        #   - game master file in json format
        # modify:
        #   - fills in pokedex
        #       - key: "xxxx" or "xxxx_name_form"
        #              where xxxx is the pokemon name (lower case)
        #              and name is pokemon name (lower case)
        #              and form is the form of the pokemon (lower case)
        for item in gm["itemTemplates"]:
            template_id = item["templateId"]
            if re.match(r'^V\d{4}_POKEMON_.*?$', template_id):
                """ create the key """
                # extract the pokemon name
                template_parts = template_id.split("_")
                number_str = re.findall(r'\d{4}', template_id)
                number_str = number_str[0]
                entry_id = number_str
                entry_name = template_parts[2:]
                entry_name = "_".join(entry_name)
                index = entry_id + "_" + entry_name.lower()

                # create index
                pokedex[index] = {}

                """ set "dex number" """
                pokedex[index]["dexnum"] = int(number_str)

                """ set "name" """
                settings = item["pokemonSettings"]
                name = settings["pokemonId"]
                name = self._gm_name_correction(name)
                pokedex[index]["name"] = name

                """ set atk/def/sta """
                pokedex[index]["atk"] = \
                    settings["stats"]["baseAttack"]
                pokedex[index]["def"] = \
                    settings["stats"]["baseDefense"]
                pokedex[index]["sta"] = \
                    settings["stats"]["baseStamina"]

                """ set type1 and type2 """
                type1 = settings["type"]
                pokedex[index]["type1"] = self._gm_type_correction(type1)
                pokedex[index]["type2"] = None
                if "type2" in settings:
                    pokedex[index]["type2"] = \
                        self._gm_type_correction(settings["type2"])

    def _gm_name_correction(self, name):
        # correcting name for name searching
        if name == "MR_MIME":
            name = "MR. MIME"
        elif name == "FARFETCHD":
            name = "FARFETCH'D"
        elif name == "NIDORAN_FEMALE":
            name = "Nidoran\u2640"
        elif name == "NIDORAN_MALE":
            name = "Nidoran\u2642"
        return name.title()

    def _gm_type_correction(self, typename):
        typename = re.sub(r'POKEMON_TYPE_', r'', typename)
        return typename.lower()
