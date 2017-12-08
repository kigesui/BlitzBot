from ..i_module import IModule, ExecResp
from utils.bot_config import BotConfig
# import random
import re

from discord import Embed


class FetchModule(IModule):

    def __init__(self):
        return

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]
        if command == "ns":
            if not re.match("^ns$", cmd):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}ns".format(
                                    BotConfig().get_botprefix())
                return [ExecResp(code=500, args=embed)]

            url = "https://i.imgur.com/XR3zFoU.jpg"
            return [ExecResp(code=210, args=url)]

        return None
