from abc import ABCMeta, abstractmethod
from collections import namedtuple


class ExecArgs(namedtuple('ExecArgs', [ "client", "rqt_msg"])):
    """
    Class passed in execute function
    """
    def __new__(cls, client=None, rqt_msg=None):
        return super(ExecArgs, cls).__new__(cls, client, rqt_msg)


class ExecResp(namedtuple('ExecResp', [ "code", "args"])):
    """
    Class returned by execute function
    """
    def __new__(cls, code=-1, args=None):
        # code
        # -1 = not set
        # 6 = shutdown
        # 200 = success, outputs embed text, args = embed
        # 210 = success, outputs normal text, args = normal text
        # 220 = success, react with emoji, args = discord.Emoji
        # 240 = success, upload picture, args = filepath
        # 300 = warning permission error, not owner
        # 500 = error, command can't be parsed
        return super(ExecResp, cls).__new__(cls, code, args)


class IModule:
    """
    Abstract Class for all modules
    """
    __metaclass__ = ABCMeta

    """
    execute returns a list of ExecResp
    """
    @abstractmethod
    def execute(self, cmd, exec_args):
        raise NotImplementedError
