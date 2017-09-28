import discord
# from discord.ext.commands import Bot
# from discord.ext import commands
from time import strftime, localtime

from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.module_loader import ModuleLoader


def main():
    BotLogger().debug("Starting script ...")

    client = discord.Client()
    modules = ModuleLoader().load_modules()

    # Redefining when bot starts
    @client.event
    async def on_ready():
        BotLogger().info("Bot Online!")
        BotLogger().info("Name: {}".format(client.user.name))
        BotLogger().info("ID: {}".format(client.user.id))
        BotLogger().info("Time: {}".format(
                         strftime("%a, %d %b %Y %H:%M:%S GMT", localtime())))
        BotLogger().info("----------")

    # Redefining when bot receive message
    @client.event
    async def on_message(request):
        # ignore non-prefix
        prefix = BotConfig().get("Defaults", "BotPrefix")
        if not request.content.startswith(prefix):
            return

        BotLogger().info("Author: {}".format(request.author))
        BotLogger().info("Server: {}".format(request.server))
        BotLogger().info("Channel: {}".format(request.channel))
        BotLogger().info("Content: {}".format(request.content))

        is_success = False
        for module in modules:
            embed = module.execute(request.content, client)

            if embed:
                is_success = True
                await client.send_message(request.channel, embed=embed)
                BotLogger().info(
                    "Command Executed: {}".format(request.content))

        if is_success is False:
            response = "Invalid Command: {}".format(request.content)
            embed = discord.Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnError")
            embed.description = response
            await client.send_message(request.channel, embed=embed)
            BotLogger().error(response)

        BotLogger().info("----------")

    # run the program
    client.run(BotConfig().get("Keys", "Token"))


if __name__ == "__main__":
    main()
