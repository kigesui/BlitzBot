from putils import Singleton

import json
import os
import re


class Pokedex(Singleton):

    GM_FILE = "gm-0.98.1.json"

    def __init__(self):
        self.__dict = self._load_dex_from_gm()

    def get_dictionary(self):
        return self._load_dex_from_gm()

    def get_all_names(self):
        return nil

    def get_stats_from_number(self, number):
        if number in self.__dict:
            attack = self.__dict[number]["atk"]
            defence = self.__dict[number]["def"]
            stamina = self.__dict[number]["sta"]
            return (attack, defence, stamina)
        return None

    def get_name_from_number(self, number):
        if number in self.__dict:
            return self.__dict[number]["name"]
        return None

    def _load_dex_from_gm(self):
        file = \
            os.path.dirname(os.path.realpath(__file__)) \
            + "/gamemaster/" + self.GM_FILE
        pokedex = {}
        with open(file, 'r') as fp:
            gm = json.loads(fp.read())
            for item in gm["itemTemplates"]:
                template_id = item["templateId"]
                if re.match(r'^V\d{4}_POKEMON_.*?$', template_id):
                    # print(template_id)
                    settings = item["pokemonSettings"]
                    number = re.findall(r'\d{4}', template_id)
                    number = int(number[0])
                    pokedex[number] = {}
                    name = settings["pokemonId"]
                    name = self._name_correction(name)
                    pokedex[number]["name"] = name

                    pokedex[number]["atk"] = \
                        settings["stats"]["baseAttack"]
                    pokedex[number]["def"] = \
                        settings["stats"]["baseDefense"]
                    pokedex[number]["sta"] = \
                        settings["stats"]["baseStamina"]

                    type1 = settings["type"]
                    pokedex[number]["type1"] = self._type_correction(type1)
                    pokedex[number]["type2"] = None
                    if "type2" in settings:
                        pokedex[number]["type2"] = \
                            self._type_correction(settings["type2"])
            # end for
            return pokedex

    def _name_correction(self, name):
        # title case
        if name == "MR_MIME":
            name = "MR. MIME"
        elif name == "FARFETCHD":
            name = "FARFETCH'D"
        elif name == "NIDORAN_FEMALE":
            name = "Nidoran\u2640"
        elif name == "NIDORAN_MALE":
            name = "Nidoran\u2642"
        return name.title()

    def _type_correction(self, typename):
        typename = re.sub(r'POKEMON_TYPE_', r'', typename)
        return typename.lower()
