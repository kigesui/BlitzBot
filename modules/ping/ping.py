from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
import re
import time

from discord import Emoji


class PingModule(IModule):

    def __init__(self):
        self.emoji = Emoji(
            require_colons = False,
            managed = False,
            id = 360233537317634058,
            name = "dogeflower",
            roles = [],
            server = None)

        return

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        command = cmd_args[0]

        if command == "ping":
            msg = "Pong! {}".format(self.emoji)
            return [ExecResp(code=210, args=msg)]

        if command == "ping2":
            msg = "Pong! {}".format(self.emoji)
            embed = EmbedHelper.success(msg)
            return [ExecResp(code=200, args=embed)]

        if command == "timer":
            if not re.match("^timer [0-9]+$", cmd):
                prefix = BotConfig.get_botprefix()
                msg = "Usage: {}timer 3".format(prefix)
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]
            # msg = "{} has set a timer.".format(exec_args.rqt_msg.author)
            # embed = EmbedHelper.success(msg)
            # channel = exec_args.rqt_msg.channel
            # exec_args.client.send_message(channel, embed=embed)
            time.sleep(int(cmd_args[1]))
            msg = "Wake up! {}".format(exec_args.rqt_msg.author.mention)
            embed = EmbedHelper.success(msg)
            return [ExecResp(code=200, args=embed)]

        if command == "hentai":
            usr = exec_args.rqt_msg.author
            hen = '\U0001F414'
            tai = '\U0001F454'
            msg = "{} {}{}".format(usr.mention, hen, tai)
            embed = EmbedHelper.success(msg)
            return [ExecResp(code=200, args=embed)]

        if command == "die":
            if exec_args.rqt_msg.author.id not in BotConfig().get_owners():
                return [ExecResp(code=300)]

            msg = "Shutting Down..."
            embed = EmbedHelper.success(msg)
            return [ExecResp(code=6, args=embed)]

        return None
