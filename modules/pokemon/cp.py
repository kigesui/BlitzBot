from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
import re
from discord import Embed


class CpModule(IModule):

    def __init__(self):
        pass

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        command = ' '.join(cmd_args[0:])

        if re.match("cp [a-zA-Z]+$", command):
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = "place holder"
            return ExecResp(code=200, embed=embed)
        return ExecResp(code=500)

    def get_cps(self):
        return {1: 123, 2: 234}
