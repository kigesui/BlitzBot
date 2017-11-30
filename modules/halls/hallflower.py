from ..i_module import IModule, ExecResp
from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_db import BotDB
from utils.bot_embed_helper import EmbedHelper
from utils.utils import get_servername

from discord import Emoji


class HallFlower(IModule):

    def __init__(self):
        self.__check_table()
        self.__load_table()

        self.__emoji = Emoji(
            require_colons = False,
            managed = False,
            id = 360233537317634058,
            name = "dogeflower",
            roles = [],
            server = None)

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
            CREATE TABLE IF NOT EXISTS hallFlower (
              user_id text NOT NULL,
              amount integer,
              PRIMARY KEY (user_id)
            );
            ''')
        cxn.commit()
        cxn.close()
        return

    def __save_table(self):
        BotLogger().debug("saving flower hall")
        # connect and get cursor
        cxn = BotDB().get_connection()
        curs = cxn.cursor()
        # drop table
        curs.execute(
            """
            DELETE FROM hallFlower
            """)
        # dict to query
        for user_id, amount in self.__hall_flower.items():
            curs.execute(
                """
                INSERT INTO hallFlower
                  VALUES (?, ?)
                """, (user_id, amount))
        # commit and close connection
        cxn.commit()
        cxn.close()
        return

    def __load_table(self):
        BotLogger().debug("getting flower hall")
        cxn = BotDB().get_connection()
        curs = cxn.cursor()
        # sql query
        ret_val = curs.execute(
            '''
            SELECT *
              FROM hallFlower
              ORDER BY amount
            ''')
        # make ret_val a dict
        self.__hall_flower = {}
        for row in ret_val:
            self.__hall_flower[row[0]] = row[1]
        # close
        cxn.close()
        return

    """
    EXECUTE
    """
    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        # """
        # show flower leader board
        # """
        if cmd_args[0] == "lbf" or cmd_args[0] == "leaderboardflower":
            # check args
            if len(cmd_args) != 1:
                prefix = BotConfig().get_botprefix()
                msg = "Usage: {}leaderboardflower or {}lbp".format(
                      prefix, prefix)
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            # refresh table
            self.__load_table()

            # create embed
            embed = EmbedHelper.success()
            embed.title = "{} Hall of Dogeflower {}".format(
                          self.__emoji, self.__emoji)
            # add each person flower
            sorted_flower = [(k, self.__hall_flower[k])
                             for k in sorted(
                             self.__hall_flower,
                             key=self.__hall_flower.get,
                             reverse=True)]

            # print the table
            rank = 0
            for user_id, user_flower in sorted_flower:
                rank += 1
                # get username
                username = get_servername(exec_args.rqt_msg.server, user_id)
                # add to leaderboard
                embed.add_field(name="#{} {}".format(rank, username),
                                value="{} {}".format(user_flower,
                                                     self.__emoji),
                                inline=True)
            # return
            return [ExecResp(code=200, args=embed)]

        # """
        # show self amount
        # """
        elif cmd_args[0] == "$":
            # check args
            if not (len(cmd_args) == 1 or
                    (len(cmd_args) == 2 and
                     len(exec_args.rqt_msg.mentions) == 1)):
                msg = "Usage: {}$ or {}$ @someone".format(prefix, prefix)
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            # refresh table
            self.__load_table()

            # get user with amount
            if exec_args.rqt_msg.mentions:
                tgt_usr = exec_args.rqt_msg.mentions[0]
            else:
                tgt_usr = exec_args.rqt_msg.author

            if tgt_usr.id in self.__hall_flower:
                amount = self.__hall_flower[tgt_usr.id]
            else:
                amount = 0

            # create embed
            msg = "{} has {} {}".format(
                  tgt_usr.mention, amount, self.__emoji)
            embed = EmbedHelper.success(msg)
            return [ExecResp(code=200, args=embed)]

        # """
        # throw flower
        # """
        elif cmd_args[0] == "give" or cmd_args[0] == "giveflower":
            ''' throw stuff at someone '''
            # BotLogger().debug(cmd_args)
            # BotLogger().debug(exec_args.rqt_msg.mentions)
            if not (len(cmd_args) == 2 and
                    len(exec_args.rqt_msg.mentions) == 1):
                msg = "Usage: {}giveflower @someone".format(
                      BotConfig().get_botprefix() )
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            src_usr = exec_args.rqt_msg.author
            tgt_usr = exec_args.rqt_msg.mentions[0]
            amount = 1

            # save to leaderboard
            if tgt_usr.id in self.__hall_flower:
                self.__hall_flower[tgt_usr.id] += int(amount)
            else:
                self.__hall_flower[tgt_usr.id] = int(amount)
            self.__save_table()

            src_usr_nick = get_servername(exec_args.rqt_msg.server, src_usr.id)

            # create response
            msg = "**{}** gave {} {} to {}.".format(
                  src_usr_nick, amount, self.__emoji,
                  tgt_usr.mention)
            embed = EmbedHelper.success(msg)
            return [ExecResp(code=200, args=embed)]

        # """
        # take flower
        # """
        elif cmd_args[0] == "take" or cmd_args[0] == "takeflower":
            ''' remove flower from someone '''
            # check parsing
            if (len(cmd_args) != 3 or
               len(exec_args.rqt_msg.mentions) == 0 or
               not cmd_args[1].isdecimal()):
                msg = "Usage: {}take 1 @someone".format(
                      BotConfig().get_botprefix() )
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            # check bot owner
            if exec_args.rqt_msg.author.id not in BotConfig().get_owners():
                return [ExecResp(code=300)]

            src_usr = exec_args.rqt_msg.author
            tgt_usr = exec_args.rqt_msg.mentions[0]
            amount = cmd_args[1]

            # save to leaderboard
            if tgt_usr.id in self.__hall_flower:
                new_amount = self.__hall_flower[tgt_usr.id] - int(amount)
                self.__hall_flower[tgt_usr.id] = max(0, new_amount)
            else:
                self.__hall_flower[tgt_usr.id] = 0
            self.__save_table()

            src_usr_nick = get_servername(exec_args.rqt_msg.server, src_usr.id)

            # create response
            msg = "**{}** pulled {} {} from {}.".format(
                  src_usr_nick, amount, self.__emoji,
                  tgt_usr.mention)
            embed = EmbedHelper.success(msg)
            return [ExecResp(code=200, args=embed)]

        return None
