# from utils.bot_logger import BotLogger
import math


class PokeStats():

    __WILD_CP_LIMIT = 35

    __LVL_MULTIPLIER = [
        0.094, 0.16639787, 0.21573247, 0.25572005, 0.29024988,
        0.3210876, 0.34921268, 0.37523559, 0.39956728, 0.42250001,
        0.44310755, 0.46279839, 0.48168495, 0.49985844, 0.51739395,
        0.53435433, 0.55079269, 0.56675452, 0.58227891, 0.59740001,
        0.61215729, 0.62656713, 0.64065295, 0.65443563, 0.667934,
        0.68116492, 0.69414365, 0.70688421, 0.71939909, 0.7317,
        0.73776948, 0.74378943, 0.74976104, 0.75568551, 0.76156384,
        0.76739717, 0.7731865, 0.77893275, 0.78463697, 0.79030001]

    def __init__(self):
        stats_file = "./modules/pokemon/stats.txt"
        self.__pokemon_stats = self.__load_stats(stats_file)
        return

    def __load_stats(self, file):
        # returns a dictionary where the pokemon name is the key
        # the value is another dictionary, with key "atk", "def", "sta"
        stats = {}
        with open(file) as fp:
            lines = fp.read().splitlines()
            for line in lines:
                line_items = line.split()
                poke = line_items[0].lower()
                stats[poke] = {}
                stats[poke]["atk"] = int(line_items[1])
                stats[poke]["def"] = int(line_items[2])
                stats[poke]["sta"] = int(line_items[3])
        return stats

    def contains(self, pokemon):
        return pokemon in self.__pokemon_stats

    def compute_cp(self, level,
                   base_atk, base_def, base_sta,
                   iv_atk=15, iv_def=15, iv_sta=15):
            m = self.__LVL_MULTIPLIER[level - 1]
            atk = (base_atk + iv_atk) * m
            defen = (base_def + iv_def) * m
            sta = (base_sta + iv_sta) * m
            cp = max(10, math.floor(math.sqrt(atk * atk * defen * sta) / 10))
            return cp

    def compute_hp(self, level, base_sta, iv_sta=15):
            m = self.__LVL_MULTIPLIER[level - 1]
            sta = (base_sta + iv_sta) * m
            hp = max(10, math.floor(sta))
            return hp

    def get_wild_poke_cps(self, pokemon, iv_atk=15, iv_def=15, iv_sta=15):
        # return key-value pairs:
        # key = level, value = cp for that level
        pokemon_stat = self.__pokemon_stats[pokemon]
        base_atk = pokemon_stat["atk"]
        base_def = pokemon_stat["def"]
        base_sta = pokemon_stat["sta"]
        out = {}
        for lvl in range(1, self.__WILD_CP_LIMIT+1):
            out[lvl] = self.compute_cp(lvl, base_atk, base_def, base_sta,
                                        iv_atk, iv_def, iv_sta)
        return out

    def get_wild_poke_hps(self, pokemon, iv_sta=15):
        pokemon_stat = self.__pokemon_stats[pokemon]
        base_sta = pokemon_stat["sta"]
        out = {}
        for lvl in range(1, self.__WILD_CP_LIMIT+1):
            out[lvl] = self.compute_hp(lvl, base_sta, iv_sta)
        return out
