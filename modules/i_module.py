from abc import ABCMeta, abstractmethod
from collections import namedtuple


class ExecArgs(namedtuple('ExecArgs', [ "client", "rqt_msg"])):
    """
    Class passed in execute function
    """
    def __new__(cls, client=None, rqt_msg=None):
        return super(ExecArgs, cls).__new__(cls, client, rqt_msg)


class ExecResp(namedtuple('ExecResp', [ "code", "embed"])):
    """
    Class returned by execute function
    """
    def __new__(cls, code=-1, embed=None):
        # code
        # -1 = not set
        # 6 = shutdown
        # 200 = success, one embed
        # 201 = success, list of embed
        # 230 = success, react with emoji
        # 250 = success, upload picture
        # 300 = warning permission error, not owner
        # 500 = error, command does not belong to module
        # 501 = error, command can't be parsed
        return super(ExecResp, cls).__new__(cls, code, embed)


class IModule:
    """
    Abstract Class for all modules
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, cmd, exec_args):
        raise NotImplementedError
