import discord
# from discord.ext.commands import Bot
# from discord.ext import commands
from time import strftime, localtime

from modules.i_module import ExecArgs
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.module_loader import ModuleLoader


def main():
    BotLogger().debug("Starting script ...")
    # BotLogger().debug("Owners: {}".format(BotConfig().get_owners()))
    # return

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

        # prepare execute function
        command = request.content[1:]
        exec_args = ExecArgs(client=client, rqt_msg=request)

        is_success = False
        for module in modules:
            # main execute function
            exec_resp = module.execute(command, exec_args)

            if exec_resp.code == 500:
                # command not from module
                continue

            elif exec_resp.code == 200:
                is_success = True
                await client.send_message(
                    request.channel, embed=exec_resp.embed)
                BotLogger().info(
                    "Command Executed Success: {}".format(request.content))

            elif exec_resp.code == 300:
                is_success = True
                await client.send_message(
                    request.channel, embed=exec_resp.embed)
                BotLogger().info(
                    "Command Executed Warning: {}".format(request.content))

            elif exec_resp.code == 6:
                # shut down
                BotLogger().info("Shutting down the bot")
                is_success = True
                await client.send_message(
                    request.channel, embed=exec_resp.embed)
                await client.logout()
                await client.close()
                BotLogger().info(
                    "Command Executed: {}".format(request.content))

            else:
                BotLogger().critical(
                    "INVALID ExecResp CODE: {}".format(exec_resp.code))
        # end for module in modules

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
