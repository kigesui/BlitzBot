from ..i_module import IModule, ExecResp
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_db import BotDB

from discord import Embed


class HallsModule(IModule):

    def __init__(self):
        self.__load_tables()
        self.__poop_emoji = '\U0001F4A9'
        return

    def __save_tables(self):
        BotDB().save('hallPoop', self.__hall_poop)
        return

    def __load_tables(self):
        self.__hall_poop = BotDB().get('hallPoop')
        return

    def __get_emoji_poop(self, client):
        for emoji in client.get_all_emojis():
            BotLogger().debug("name:{}".format(emoji.name))
            BotLogger().debug("id:{}".format(emoji.id))
            BotLogger().debug("require_colons:{}".format(emoji.require_colons))
            BotLogger().debug("url:{}".format(emoji.url))

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        # """
        # show poop leader board
        # """
        if cmd_args[0] == "lbp" or cmd_args[0] == "leaderboardpoop":
            # check args
            if len(cmd_args) != 1:
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                prefix = BotConfig().get_botprefix()
                embed.description = "Usage: {}leaderboardpoop or {}lbp".format(
                                    prefix, prefix)
                return ExecResp(code=501, embed=embed)

            # refresh table
            self.__load_tables()

            # create embed
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.title = "{} Hall of Poop {}".format(self.__poop_emoji,
                                                      self.__poop_emoji)
            # add each person poop
            sorted_poop = [(k, self.__hall_poop[k])
                           for k in sorted(
                           self.__hall_poop,
                           key=self.__hall_poop.get,
                           reverse=True)]

            server = exec_args.rqt_msg.server
            rank = 0
            for user_id, user_poop in sorted_poop:
                rank += 1
                # get username
                username = "{}".format(user_id)
                if server:
                    member = server.get_member(user_id)
                    if member:
                        username = member.name
                        if member.nick:
                            username = member.nick
                # add to leaderboard
                embed.add_field(name="#{} {}".format(rank, username),
                                value="{} {}".format(user_poop,
                                                     self.__poop_emoji),
                                inline=True)
            # return
            return ExecResp(code=200, embed=embed)

        # """
        # show self amount
        # """
        elif cmd_args[0] == "$":
            # check args
            if len(cmd_args) != 1:
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                prefix = BotConfig().get_botprefix()
                embed.description = "Usage: {}$".format(prefix)
                return ExecResp(code=501, embed=embed)

            # refresh table
            self.__load_tables()

            # get user with amount
            src_usr = exec_args.rqt_msg.author
            amount = self.__hall_poop[src_usr.id]

            # create embed
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = "{} has {} {}".format(
                                src_usr, amount, self.__poop_emoji)
            return ExecResp(code=200, embed=embed)

        # """
        # throw poop
        # """
        elif cmd_args[0] == "throwpoop":
            ''' throw stuff at someone '''
            # BotLogger().debug(cmd_args)
            # BotLogger().debug(exec_args.rqt_msg.mentions)
            if (len(cmd_args) != 3 or
               len(exec_args.rqt_msg.mentions) == 0 or
               not cmd_args[1].isdecimal()):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}throwpoop 1 @someone".format(
                                    BotConfig().get_botprefix() )
                return ExecResp(code=501, embed=embed)

            src_usr = exec_args.rqt_msg.author
            tgt_usr = exec_args.rqt_msg.mentions[0]
            amount = cmd_args[1]

            # save to leaderboard
            if tgt_usr.id in self.__hall_poop:
                self.__hall_poop[tgt_usr.id] += int(amount)
            else:
                self.__hall_poop[tgt_usr.id] = int(amount)
            self.__save_tables()

            # create response
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = "{} throw {} {} at {}.".format(
                                src_usr, amount, self.__poop_emoji,
                                tgt_usr.mention)
            return ExecResp(code=200, embed=embed)

        return ExecResp(code=500)
