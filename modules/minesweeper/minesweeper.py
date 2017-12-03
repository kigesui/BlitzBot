from ..i_module import IModule, ExecResp
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper
# from utils.bot_logger import BotLogger
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
            if not re.match("^ms (beginner|intermediate)$", cmd):
                embed = EmbedHelper.error(
                    "Usage: {}ms beginner|intermediate".format(
                        BotConfig().get_botprefix()))
                return [ExecResp(code=500, args=embed)]

            level = cmd_args[1]
            if level == "beginner":
                w = 8
                h = 8
                m = 10
            elif level == "intermediate":
                w = 16
                h = 16
                m = 40
            else:
                w = 1
                h = 1
                m = 1

            return self.start_game(w, h, m)

        # reveal
        if command == "msr":
            if not re.match("^msr [A-Za-z][0-9]+$", cmd):
                msg = "Usage: {}msr A1".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            x, y = self.convert_input(cmd_args[1])
            return self.reveal(x, y)

        # expand
        if command == "mse":
            if not re.match("^mse [A-Za-z][0-9]+$", cmd):
                msg = "Usage: {}mse A1".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            x, y = self.convert_input(cmd_args[1])
            return self.expand(x, y)

        # flag
        if command == "msf":
            if not re.match("^msf [A-Za-z][0-9]+$", cmd):
                msg = "Usage: {}msf A1".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]

            x, y = self.convert_input(cmd_args[1])
            return self.flag(x, y)

        if command == "msd":
            if not re.match("^msd$", cmd):
                msg = "Usage: {}msd".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]
            return self.display_board()

        elif command == "mss":
            if not re.match("^mss$", cmd):
                msg = "Usage: {}mss".format(
                      BotConfig().get_botprefix())
                embed = EmbedHelper.error(msg)
                return [ExecResp(code=500, args=embed)]
            return self.stop_game()

        return None
    # end of execute

    # convert input
    def convert_input(self, user_input):
        x = ord(user_input[0].upper()) - 0x40
        y = int(user_input[1:])
        return (x, y)

    # decorator to check if game is running or not
    def game_running(want_run=True):
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

    # decorator to display board
    def add_display(func):
        def func_warpper(self, *arg, **kw):
            func_list = func(self, *arg, **kw)
            board = self.display_board()
            return func_list + board
        return func_warpper

    # decorator to check if win or lose
    def check_win_lose(func):
        def func_warpper(self, *arg, **kw):
            # BotLogger().info("checked")
            ret_list = func(self, *arg, **kw)
            if self.__board.game_lose():
                embed = EmbedHelper.success("Game Over! Try Again.")
                ret_list.append(ExecResp(code=200, args=embed))
            if self.__board.game_won():
                embed = EmbedHelper.success("Congratulation! You Won.")
                ret_list.append(ExecResp(code=200, args=embed))
            return ret_list
        return func_warpper

    # all functions below are called after parsing
    @game_running(False)
    @check_win_lose
    @add_display
    def start_game(self, w, h, m):
        self.__board = Board()
        self.__board.init(w, h, m)
        embed = EmbedHelper.success("Minesweeper Start!")
        return [ExecResp(code=200, args=embed)]

    @game_running()
    @add_display
    def stop_game(self):
        self.__board = None
        embed = EmbedHelper.success("Minesweeper Stopped.")
        return [ExecResp(code=200, args=embed)]

    @game_running()
    def display_board(self):
        embed = EmbedHelper.success( "```" + str(self.__board) + "```")
        return [ExecResp(code=200, args=embed)]

    @game_running()
    @add_display
    def flag(self, x, y):
        x_str = chr(x+0x40)
        if self.__board.flag(x, y):
            embed = EmbedHelper.success("Flagged {0}{1}".format(x_str, y))
        else:
            embed = EmbedHelper.warning("{0}{1} is revealed or invalid"
                                        .format(x_str, y))
        return [ExecResp(code=200, args=embed)]

    @game_running()
    @check_win_lose
    @add_display
    def reveal(self, x, y):
        x_str = chr(x+0x40)
        if self.__board.reveal(x, y):
            embed = EmbedHelper.success("Revealed {0}{1}".format(x_str, y))
        else:
            embed = EmbedHelper.warning("{0}{1} already revealed or invalid"
                                        .format(x_str, y))
        return [ExecResp(code=200, args=embed)]

    @game_running()
    @check_win_lose
    @add_display
    def expand(self, x, y):
        x_str = chr(x+0x40)
        if self.__board.expand(x, y):
            embed = EmbedHelper.success("Expanded {0}{1}".format(x_str, y))
        else:
            embed = EmbedHelper.warning("{0}{1} cannot be expanded"
                                        .format(x_str, y))
        return [ExecResp(code=200, args=embed)]
