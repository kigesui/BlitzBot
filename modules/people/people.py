from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig


class PeopleModule(IModule):

    def __init__(self):
        pass

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        # ignore if there are arguments
        if len(cmd_args) > 1:
            return ExecResp(code=500)

        command = cmd_args[0]

        if command == "blazikeen":
            filepath = "./modules/people/pics/blazikeen.gif"
            return ExecResp(code=250, embed=filepath)

        if command == "peetarded":
            filepath = "./modules/people/pics/peetarded.gif"
            return ExecResp(code=250, embed=filepath)

        if command == "maoke":
            filepath = "./modules/people/pics/maoke.png"
            return ExecResp(code=250, embed=filepath)

        return ExecResp(code=500)
