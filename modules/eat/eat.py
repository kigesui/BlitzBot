from ..i_module import IModule, ExecResp
from utils.bot_config import BotConfig
import random
import re

from discord import Embed


class EatModule(IModule):

    def __init__(self):
        self.__list = self._get_restaurants()
        return

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]
        if command == "eat":
            if not re.match("^eat$", cmd):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}eat".format(
                                    BotConfig().get_botprefix())
                return [ExecResp(code=500, args=embed)]

            choice = random.choice(self.__list)
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = str(choice)
            return [ExecResp(code=200, args=embed)]

        return None

    def _get_restaurants(self):
        file = "./modules/eat/places.txt"
        restaurant_list = []
        with open(file) as fp:
            all_lines = fp.read().splitlines()
            for line in all_lines:
                if not line:  # ignore empty line
                    continue
                line = line.strip()  # remove white space
                if line.startswith("#"):  # ignore comments
                    continue
                restaurant_list.append(line)
        return restaurant_list
