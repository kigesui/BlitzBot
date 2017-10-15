from ..i_module import IModule, ExecResp

from modules.halls.hallpoop import HallPoop
from modules.halls.hallflower import HallFlower


class HallsModule(IModule):

    def __init__(self):
        self.halls = [ HallPoop(), HallFlower() ]
        return

    def execute(self, cmd, exec_args):

        for hall in self.halls:
            exec_resp = hall.execute(cmd, exec_args)
            if exec_resp.code != 500:
                return exec_resp

        return ExecResp(code=500)
