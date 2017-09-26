import discord
from discord.ext.commands import Bot
from discord.ext import commands
from time import strftime, gmtime

from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig


def main():
    BotLogger().debug("Starting script ...")
    config = BotConfig()

    token = config.get("Keys", "Token")

    client = discord.Client()

    @client.event
    async def on_ready():
        BotLogger().info("Bot Online!")
        BotLogger().info("Name: {}".format(client.user.name))
        BotLogger().info("ID: {}".format(client.user.id))
        BotLogger().info("Time: {}".format(
                         strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())))
        BotLogger().info("----------")


# # todo: put this in config
# # bot_key = "MzU3NzU3NTc5NzcxNzcyOTM5.DJwX7w.eangOFjstHUvICCApXMzEvNFaFM"
# # bot_prefix = "!"


# @client.event
# async def on_ready():
#     print("Bot Online!")
#     print("Name: {}".format(client.user.name))
#     print("ID: {}".format(client.user.id))
#     print("Time: {}".format(strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())))
#     print("----------")


# # @client.event
# # async def on_message(msg):

# #     if not msg.content.startswith(bot_prefix):
# #         return

# #     print("Author: {}".format(msg.author))
# #     print("Server: {}".format(msg.server))
# #     print("Channel: {}".format(msg.channel))
# #     print("Content: {}".format(msg.content))







#     # parser = CommandParser()
#     # command = parser.parse(msg.content[1:])

#     # outputs = command.execute()

#     # channel = msg.channel

#     # for output in outputs:
#     #     embed = discord.Embed()
#     #     embed.colour = 0x15ac13
#     #     embed.description = output
#     #     await client.send_message(channel, embed=embed)


#     # if msg.content.startswith("!ping"):
#     #     pong_msg = "You face Botraxxus! Bot Lord of the Blitz Legion!"
#     #     await client.send_message(msg.channel, pong_msg)

#     # if msg.content.startswith("!test"):
#     #     embed = discord.Embed()
#     #     # embed.title = "title"
#     #     # embed.description = "description"
#     #     embed.colour = 0x15ac13
#     #     # embed.url = "https://www.google.com/maps?q=43.4372438479,-80.5418049229"
#     #     # for i in range(20):
#     #         # embed.add_field(name="f{}".format(i),
#     #         #                 value="v{}".format(i),
#     #         #                 inline=False)
#     #     # embed.add_field(name="f2", value="v2", inline=True)
#     #     print("Channel: {}".format(msg.channel))
#     #     await client.send_message(msg.channel, "asd", embed=embed)

    client.run(token)

#     print("----------")


if __name__ == "__main__":
    main()
