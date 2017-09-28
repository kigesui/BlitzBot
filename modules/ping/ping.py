from ..i_module import IModule
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig

import discord


class PingModule(IModule):

    def execute(self, cmd, client):
        args = cmd.split(' ')
        if args[0] == "!ping":
            msg = "Pong!"
            embed = discord.Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = msg
            return embed
        return None










