from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
from utils.bot_embed_helper import EmbedHelper


# admin decorator
def check_admin(func):
    def func_warpper(module, admin_id, *args, **kwargs):
        if admin_id not in BotConfig().get_owners():
            return [ExecResp(code=300)]
        else:
            return func(module, *args, **kwargs)
    return func_warpper


class AdminModule(IModule):

    def __init__(self):
        return

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]

        if command == "die":
            return self._handle_shutdown(exec_args.rqt_msg.author.id)

        return None

    # handle shutdown
    @check_admin
    def _handle_shutdown(self):
        msg = "Shutting Down..."
        embed = EmbedHelper.success(msg)
        return [ExecResp(code=6, args=embed)]
