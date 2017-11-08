from ..i_module import IModule, ExecResp

# from utils.bot_logger import BotLogger

from discord import Emoji


class AutoReactModule(IModule):

    def __init__(self):
        self.__emoji_hentai = Emoji(
            require_colons = False,
            managed = False,
            id = 360228298443194369,
            name = "hentai",
            roles = [],
            server = None)
        return

    def execute(self, cmd, exec_args):

        if "entai" in cmd.lower():
            return [ExecResp(code=220, embed=self.__emoji_hentai)]

        return None
