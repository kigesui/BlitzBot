from discord import Embed

from utils.bot_config import BotConfig


class EmbedHelper:

    @staticmethod
    def error(msg=None):
        embed = Embed()
        embed.colour = BotConfig().get_hex("Colors", "OnError")
        if msg:
            embed.description = msg
        return embed

    @staticmethod
    def success(msg=None):
        embed = Embed()
        embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
        if msg:
            embed.description = msg
        return embed

    @staticmethod
    def warning(msg=None):
        embed = Embed()
        embed.colour = BotConfig().get_hex("Colors", "OnWarning")
        if msg:
            embed.description = msg
        return embed
