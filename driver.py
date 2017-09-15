import discord
from discord.ext.commands import Bot
from discord.ext import commands

client = discord.Client()
bot_key = "MzU3NzU3NTc5NzcxNzcyOTM5.DJwX7w.eangOFjstHUvICCApXMzEvNFaFM"


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print("----------")


@client.event
async def on_message(msg):
    if msg.content.startswith("!ping"):
        pong_msg = "You face Botraxxus! Bot Lord of the Blitz Legion!"
        await client.send_message(msg.channel, pong_msg)

client.run(bot_key)
