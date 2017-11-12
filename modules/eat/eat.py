from ..i_module import IModule, ExecResp
import random


class EatModule(IModule):

    def __init__(self):
        self.list = ["Aunty's Kitchen", "Waterloo Star",
                        "Grace and Healthy Dumplings",
                        "Kenzo Ramen", "Harvey's",
                        "Chen's Oriental Cuisine",
                        "Seoul Soul", "Lazeez",
                        "Mikey's Eatery", "The Pita Factory",
                        "Kismet Restaurant", "Sogo", "Burger King",
                        "Linden Square"]
        pass

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]
        if command == 'eat':
            choice = random.choice(self.list)
            return [ExecResp(code=210, args=choice)]

        return None
