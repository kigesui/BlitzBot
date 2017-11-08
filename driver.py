import discord
# from discord.ext.commands import Bot
# from discord.ext import commands
from time import strftime, localtime
import traceback

from modules.i_module import ExecArgs
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_db import BotDB
from utils.module_loader import ModuleLoader


def main():
    BotLogger().info("Starting Bot ...")

    # init some global values
    BOT_PREFIX = BotConfig().get_botprefix()

    BotLogger().info("Bot Prefix: {}".format(BOT_PREFIX))
    BotLogger().info("Bot Owners: {}".format(BotConfig().get_owners()))

    client = discord.Client()
    playing_status = "{} prefix".format(BOT_PREFIX)

    BotLogger().info("Loading Modules")
    CMD_MODULES, AUTO_MODULES = ModuleLoader().load_all_modules()

    # Redefining when bot starts
    @client.event
    async def on_ready():
        BotLogger().info("----------")
        BotLogger().info("Bot Online!")
        BotLogger().info("Name: {}".format(client.user.name))
        BotLogger().info("ID: {}".format(client.user.id))
        BotLogger().info("Time: {}".format(
                         strftime("%a, %d %b %Y %H:%M:%S GMT", localtime())))
        await client.change_presence(game=discord.Game(name=playing_status))

    # Redefining when bot receive message
    @client.event
    async def on_message(request):

        # ignore if its lenght 1, fix for just "!"
        if len(request.content) <= 1:
            return

        # init: prepare args
        exec_args = ExecArgs(client=client, rqt_msg=request)

        """ First Round of Content Parsing
            - try to parse with auto modules (content without bot prefix)
        """
        for module in AUTO_MODULES:
            # main execute function
            exec_resps = module.execute(request.content, exec_args)

            # if module has response
            if exec_resps:
                retval = await handle_multi_resps(client, request, exec_resps)
                if retval == 0:
                    # handled, dont try to parse through command modules
                    return
                else:
                    # something wrong, check log
                    BotLogger().error(
                        "Something went wrong while handing {}"
                        .format(request.content))
                    return

        """ Second Round of Content Parsing
            - try to parse with command modules (content with bot prefix)
        """
        # drop those that are not command
        if request.content[0] != BOT_PREFIX:
            return

        BotLogger().info("----------")
        BotLogger().info("Author: {}".format(request.author))
        BotLogger().info("Server: {}".format(request.server))
        BotLogger().info("Channel: {}".format(request.channel))
        BotLogger().info("Content: {}".format(request.content))

        # prepare execute function
        command = request.content[1:]

        is_success = False
        for module in CMD_MODULES:
            # main execute function
            exec_resps = module.execute(command, exec_args)

            # if module has response
            if exec_resps:
                retval = await handle_multi_resps(client, request, exec_resps)
                if retval == 0:
                    is_success = True
                else:
                    # something went wrong, check log
                    is_success = False
                # command usually handled by first module in line
                break

        # couldn't figure out command, or critical error, print this
        if is_success is False:
            response = "Invalid Command: {}".format(request.content)
            embed = discord.Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnError")
            embed.description = response
            await client.send_message(request.channel, embed=embed)
            BotLogger().error(response)

    # run the program
    BotLogger().info("Running Client")
    client.run(BotConfig().get("Keys", "Token"))
    BotLogger().info("Client shut down.")
    return


async def handle_multi_resps(client, request, exec_responses):
    """ Handle a list of responses
        pass each one through the function that handles a single one
        returns:
            0   for module handled successfully, stop there
            1   for not handled by a module, continue trying
            -1  for critical error
    """
    for resp in exec_responses:
        retval = await handle_single_resp(client, request, resp)
        if retval == -1:
            return -1

    return 0


async def handle_single_resp(client, request, exec_resp):
    """ Handle a single response
        This function can only be called from async function
        returns:
            0   for module handled successfully, stop there
            1   for not handled by a module, continue trying
            -1  for critical error
    """
    if exec_resp.code == 6:
        # shut down
        BotLogger().info("Shutting down the bot")
        await client.send_message(
            request.channel, embed=exec_resp.embed)
        await client.logout()
        await client.close()
        BotLogger().info("Bot is closed.")
        return 0

    elif exec_resp.code == 200:
        await client.send_message(
            request.channel, embed=exec_resp.embed)
        BotLogger().info(
            "Command Executed Success: {}".format(request.content))
        return 0

    elif exec_resp.code == 201:
        for e in exec_resp.embed:
            await client.send_message(
                request.channel, embed=e)
        BotLogger().info(
            "Command Executed Success: {}".format(request.content))
        return 0

    elif exec_resp.code == 220:
        emoji = exec_resp.embed
        message = request
        BotLogger().info("Adding Reaction: {}".format(emoji))
        await client.add_reaction(request, emoji)
        BotLogger().info("Command Executed Success: {}"
                         .format(request.content))
        return 0

    elif exec_resp.code == 240:
        filepath = exec_resp.embed
        BotLogger().info("Uploading File: {}".format(filepath))
        with open(filepath, 'rb') as f:
            await client.send_file(request.channel, f)
        BotLogger().info("Command Executed Success: {}"
                         .format(request.content))
        return 0

    elif exec_resp.code == 300:
        BotLogger().warning("Permission Error")

        # # dont say anything
        # embed = discord.Embed()
        # embed.colour = BotConfig().get_hex("Colors", "OnWarning")
        # embed.description = "You are not the boss of me!"
        # await client.send_message(request.channel, embed=embed)

        BotLogger().warning("Need to be bot owner: {}".format(request.content))
        return 0

    elif exec_resp.code == 500:
        BotLogger().error("Parsing Error")
        await client.send_message(
            request.channel, embed=exec_resp.embed)
        BotLogger().error(
            "Command Parsing Error: {}".format(request.content))
        return 0

    else:
        BotLogger().critical(
            "INVALID ExecResp CODE: {}".format(exec_resp.code))
        return -1


# main function call
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        BotLogger().error(traceback.format_exc())
