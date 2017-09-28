from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig

from discord import Embed


class PingModule(IModule):

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        if cmd_args[0] == "ping":
            msg = "Pong!"
            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = msg
            return ExecResp(code=200, embed=embed)

        if cmd_args[0] == "die":
            author_id = exec_args.rqt_msg.author.id
            if author_id in BotConfig().get_owners():
                msg = "Shutting Down..."
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
                embed.description = msg
                return ExecResp(code=6, embed=embed)
            else:
                msg = "You are not the boss of me!"
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnWarning")
                embed.description = msg
                return ExecResp(code=300, embed=embed)

        return ExecResp(code=500)
