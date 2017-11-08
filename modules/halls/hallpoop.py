from ..i_module import IModule, ExecResp
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_db import BotDB
from utils.utils import get_servername

from discord import Embed


class HallPoop(IModule):

    def __init__(self):
        self.__check_table()
        self.__load_table()
        self.__emoji = '\U0001F4A9'
        return

    """
    SQL STUFF
    """
    def __check_table(self):
        # create it if not present
        cxn = BotDB().get_connection()
        curs = cxn.cursor()
        curs.execute(
            '''
            CREATE TABLE IF NOT EXISTS hallPoop (
              user_id text NOT NULL,
              amount integer,
              PRIMARY KEY (user_id)
            );
            ''')
        cxn.commit()
        cxn.close()
        return

    def __save_table(self):
        BotLogger().debug("saving poop hall")
        # connect and get cursor
        cxn = BotDB().get_connection()
        curs = cxn.cursor()
        # drop table
        curs.execute(
            """
            DELETE FROM hallPoop
            """)
        # dict to query
        for user_id, amount in self.__hall_poop.items():
            curs.execute(
                """
                INSERT INTO hallPoop
                  VALUES (?, ?)
                """, (user_id, amount))
        # commit and close connection
        cxn.commit()
        cxn.close()
        return

    def __load_table(self):
        BotLogger().debug("getting poop hall")
        cxn = BotDB().get_connection()
        curs = cxn.cursor()
        # sql query
        ret_val = curs.execute(
            '''
            SELECT *
              FROM hallPoop
              ORDER BY amount
            ''')
        # make ret_val a dict
        self.__hall_poop = {}
        for row in ret_val:
            self.__hall_poop[row[0]] = row[1]
        # close
        cxn.close()
        return

    """
    EXECUTE
    """
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
                return [ExecResp(code=500, embed=embed)]

            # refresh table
            self.__load_table()

            # create embed
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.title = "{} Hall of Poop {}".format(self.__emoji,
                                                      self.__emoji)
            # add each person poop
            sorted_poop = [(k, self.__hall_poop[k])
                           for k in sorted(
                           self.__hall_poop,
                           key=self.__hall_poop.get,
                           reverse=True)]

            # print the table
            rank = 0
            for user_id, user_poop in sorted_poop:
                rank += 1
                # get username
                username = get_servername(exec_args.rqt_msg.server, user_id)
                # add to leaderboard
                embed.add_field(name="#{} {}".format(rank, username),
                                value="{} {}".format(user_poop,
                                                     self.__emoji),
                                inline=True)
            # return
            return [ExecResp(code=200, embed=embed)]

        # """
        # show self amount
        # """
        elif cmd_args[0] == "showpoop":
            # check args
            if not (len(cmd_args) == 1 or
                    (len(cmd_args) == 2 and
                     len(exec_args.rqt_msg.mentions) == 1)):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                prefix = BotConfig().get_botprefix()
                embed.description = \
                    "Usage: {}showpoop or {}showpoop @someone".format(
                        prefix, prefix)
                return [ExecResp(code=500, embed=embed)]

            # refresh table
            self.__load_table()

            # get user with amount
            if exec_args.rqt_msg.mentions:
                tgt_usr = exec_args.rqt_msg.mentions[0]
            else:
                tgt_usr = exec_args.rqt_msg.author

            if tgt_usr.id in self.__hall_poop:
                amount = self.__hall_poop[tgt_usr.id]
            else:
                amount = 0

            # create embed
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = "{} holds {} {}".format(
                                tgt_usr.mention, amount, self.__emoji)
            return [ExecResp(code=200, embed=embed)]

        # """
        # throw poop
        # """
        elif cmd_args[0] == "tp" or cmd_args[0] == "throwpoop":
            ''' throw stuff at someone '''
            # BotLogger().debug(cmd_args)
            # BotLogger().debug(exec_args.rqt_msg.mentions)
            if not (len(cmd_args) == 2 and
                    len(exec_args.rqt_msg.mentions) == 1):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}throwpoop @someone".format(
                                    BotConfig().get_botprefix() )
                return [ExecResp(code=500, embed=embed)]

            src_usr = exec_args.rqt_msg.author
            tgt_usr = exec_args.rqt_msg.mentions[0]
            amount = 1

            # save to leaderboard
            if tgt_usr.id in self.__hall_poop:
                self.__hall_poop[tgt_usr.id] += int(amount)
            else:
                self.__hall_poop[tgt_usr.id] = int(amount)
            self.__save_table()

            src_usr_nick = get_servername(exec_args.rqt_msg.server, src_usr.id)

            # create response
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = "**{}** throw {} {} at {}.".format(
                                src_usr_nick, amount, self.__emoji,
                                tgt_usr.mention)
            return [ExecResp(code=200, embed=embed)]

        # """
        # clean poop
        # """
        elif cmd_args[0] == "clean" or cmd_args[0] == "cleanpoop":
            ''' remove poop from someone '''
            # check parsing
            if (len(cmd_args) != 3 or
               len(exec_args.rqt_msg.mentions) == 0 or
               not cmd_args[1].isdecimal()):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}clean 1 @someone".format(
                                    BotConfig().get_botprefix() )
                return [ExecResp(code=500, embed=embed)]

            # check bot owner
            if exec_args.rqt_msg.author.id not in BotConfig().get_owners():
                return [ExecResp(code=300)]

            src_usr = exec_args.rqt_msg.author
            tgt_usr = exec_args.rqt_msg.mentions[0]
            amount = cmd_args[1]

            # save to leaderboard
            if tgt_usr.id in self.__hall_poop:
                new_amount = self.__hall_poop[tgt_usr.id] - int(amount)
                self.__hall_poop[tgt_usr.id] = max(0, new_amount)
            else:
                self.__hall_poop[tgt_usr.id] = 0
            self.__save_table()

            src_usr_nick = get_servername(exec_args.rqt_msg.server, src_usr.id)

            # create response
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = "**{}** took {} {} from {}.".format(
                                src_usr_nick, amount, self.__emoji,
                                tgt_usr.mention)
            return [ExecResp(code=200, embed=embed)]

        return None
