from ..i_module import IModule

from modules.halls.hallpoop import HallPoop
from modules.halls.hallflower import HallFlower


class HallsModule(IModule):

    def __init__(self):
        self.halls = [ HallPoop(), HallFlower() ]
        return

    def execute(self, cmd, exec_args):

        for hall in self.halls:
            exec_resps = hall.execute(cmd, exec_args)
            if exec_resps:
                return exec_resps

        return None
