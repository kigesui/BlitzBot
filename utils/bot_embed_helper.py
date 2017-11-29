from discord import Embed

from utils.bot_config import BotConfig


class EmbedHelper:

    @staticmethod
    def error(msg):
        embed = Embed()
        embed.colour = BotConfig().get_hex("Colors", "OnError")
        embed.description = msg
        return embed

    @staticmethod
    def success(msg):
        embed = Embed()
        embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
        embed.description = msg
        return embed

    @staticmethod
    def warning(msg):
        embed = Embed()
        embed.colour = BotConfig().get_hex("Colors", "OnWarning")
        embed.description = msg
        return embed
