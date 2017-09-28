import discord
from discord.ext.commands import Bot
from discord.ext import commands
from time import strftime, localtime

from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.module_loader import ModuleLoader


def main():
    BotLogger().debug("Starting script ...")

    # config = BotConfig()

    client = discord.Client()

    # redefining some function
    @client.event
    async def on_ready():
        BotLogger().info("Bot Online!")
        BotLogger().info("Name: {}".format(client.user.name))
        BotLogger().info("ID: {}".format(client.user.id))
        BotLogger().info("Time: {}".format(
                         strftime("%a, %d %b %Y %H:%M:%S GMT", localtime())))
        BotLogger().info("----------")

    # modules = ModuleLoader().load_modules()

    @client.event
    async def on_message(msg):
        # ignore non-prefix
        prefix = BotConfig().get("Defaults", "BotPrefix")
        if not msg.content.startswith(prefix):
            return

        BotLogger().info("Author: {}".format(msg.author))
        BotLogger().info("Server: {}".format(msg.server))
        BotLogger().info("Channel: {}".format(msg.channel))
        BotLogger().info("Content: {}".format(msg.content))

        is_success = False
        for module in modules:
            is_success = module.execute(msg.content)

            if is_success:
                break

        if is_success is False:
            embed = discord.Embed()
            embed.colour = BotConfig().get("Colors", "OnError")
            embed.description = "Invalid Command: {}".format(msg.content)
            await client.send_message(msg.channel, embed=embed)
            BotLogger().error("Invalid Command")

        BotLogger().info("----------")

    # run the program
    client.run(BotConfig().get("Keys", "Token"))


if __name__ == "__main__":
    main()
