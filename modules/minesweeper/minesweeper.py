from ..i_module import IModule, ExecResp
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
from modules.minesweeper.minesweeper_logic import Board
# import random
import re


class MinesweeperModule(IModule):

    def __init__(self):
        self.__board = None
        return

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]

        # start new game
        if command == "ms":
            if not re.match("^ms [0-9]+ [0-9]+ [0-9]+$", cmd):
                embed = EmbedHelper.error(
                    "Usage: {}ms width heigth mines".format(
                        BotConfig().get_botprefix()))
                return [ExecResp(code=500, args=embed)]

            w = int(cmd_args[1])
            h = int(cmd_args[2])
            m = int(cmd_args[3])

            return self.start_game(w, h, m)

        # reveal
        if command == "msr":
            if not re.match("^msr [A-Za-z][0-9]+$", cmd):
                msg = "Usage: {}msr A1".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            embed = EmbedHelper.warning("todo: reveal")
            return [ExecResp(code=200, args=embed)]

        # flag
        if command == "msf":
            if not re.match("^msf [A-Za-z][0-9]+$", cmd):
                msg = "Usage: {}msf A1".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            embed = EmbedHelper.warning("todo: flag")
            return [ExecResp(code=200, args=embed)]

        if command == "msd":
            if not re.match("^msd$", cmd):
                msg = "Usage: {}msd".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]
            return self.display_board(cmd)

        elif command == "mss":
            if not re.match("^mss$", cmd):
                msg = "Usage: {}mss".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]
            return self.stop_game(cmd)

        return None
    # end of execute

    # decorator to check if game is running or not
    def game_running(want_run):
        def game_running_decorator(func):
            def func_warpper(self, *arg, **kw):
                if want_run and not self.__board:
                    msg = "Minesweeper is not running."
                    embed = EmbedHelper.warning(msg)
                    return [ExecResp(code=200, args=embed)]
                if not want_run and self.__board:
                    msg = "Minesweeper is already running."
                    embed = EmbedHelper.warning(msg)
                    return [ExecResp(code=200, args=embed)]
                return func(self, *arg, **kw)
            return func_warpper
        return game_running_decorator

    @game_running(False)
    def start_game(self, w, h, m):
        self.__board = Board()
        self.__board.init(w, h, m)
        embed = EmbedHelper.success("Minesweeper Start!")
        return [ExecResp(code=200, args=embed)]

    @game_running(True)
    def stop_game(self, cmd):
        self.__board = None
        embed = EmbedHelper.success("Minesweeper Stopped.")
        return [ExecResp(code=200, args=embed)]

    @game_running(True)
    def display_board(self, cmd):
        embed = EmbedHelper.success( "```" + str(self.__board) + "```")
        return [ExecResp(code=200, args=embed)]
