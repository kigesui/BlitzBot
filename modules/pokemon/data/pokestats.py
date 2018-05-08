# from utils.bot_logger import BotLogger
from . import Pokedex
from . import IV
from putils import Singleton

import math
import os


class PokemonStats(Singleton):

    __WILD_CP_LIMIT = 35

    def __init__(self):
        self.__LVL_MULTIPLIER = {}
        cp_mult_file = \
            os.path.dirname(os.path.realpath(__file__)) \
            + "/cp_mult.csv"
        with open(cp_mult_file) as fp:
            for line in fp:
                line = line.strip()
                line_items = line.split(",")
                self.__LVL_MULTIPLIER[float(line_items[0])] = \
                    float(line_items[1])
        return

    def compute_cp(self, level,
                   base_atk, base_def, base_sta,
                   iv):
            m = self.__LVL_MULTIPLIER[level]
            atk = (base_atk + iv.attack) * m
            defen = (base_def + iv.defense) * m
            sta = (base_sta + iv.stamina) * m
            cp = max(10, math.floor(math.sqrt(atk * atk * defen * sta) / 10))
            return cp

    def compute_hp(self, level, base_sta, iv_sta=15):
            m = self.__LVL_MULTIPLIER[level]
            sta = (base_sta + iv_sta) * m
            hp = max(10, math.floor(sta))
            return hp

    def get_wild_pokemon_cps(self, number, iv=IV(0xf, 0xf, 0xf)):
        # in: pokemon number
        # out: dict where key = level,
        #                 value = cp for that level
        #      None if number is invalid
        stats = Pokedex().get_stats_from_number(number)
        if stats is None:
            return None
        base_atk, base_def, base_sta = stats
        out = {}
        for lvl in range(1, self.__WILD_CP_LIMIT+1):
            out[lvl] = self.compute_cp(lvl, base_atk, base_def, base_sta, iv)
        return out

    def get_wild_pokemon_hps(self, number, iv_sta=15):
        stats = Pokedex().get_stats_from_number(number)
        if stats is None:
            return None
        _, _, base_sta = stats
        out = {}
        for lvl in range(1, self.__WILD_CP_LIMIT+1):
            out[lvl] = self.compute_hp(lvl, base_sta, iv_sta)
        return out
