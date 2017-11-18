# from utils.bot_logger import BotLogger

# modules import
from modules.automodules.react import AutoReactModule
from modules.ping.ping import PingModule
from modules.halls.halls import HallsModule
from modules.people.people import PeopleModule
from modules.pokemon.cp import CpModule
from modules.eat.eat import EatModule
from modules.crypto.crypto import CryptoModule
from modules.ns.fetch import FetchModule


class ModuleLoader:
    class __ModuleLoader():
        def __init__(self):
            pass

        def load_auto_modules(self):
            """ Auto modules execute command without bot prefix """
            auto_modules = []
            auto_modules.append(AutoReactModule())
            return auto_modules

        def load_cmd_modules(self):
            """ Command modules execute command after bot prefix """
            cmd_modules = []
            cmd_modules.append(PingModule())
            cmd_modules.append(HallsModule())
            cmd_modules.append(PeopleModule())
            cmd_modules.append(CpModule())
            cmd_modules.append(EatModule())
            cmd_modules.append(CryptoModule())
            cmd_modules.append(FetchModule())
            return cmd_modules

    instance = None

    def __init__(self):
        if not ModuleLoader.instance:
            ModuleLoader.instance = ModuleLoader.__ModuleLoader()

    def load_all_modules(self):
        return (ModuleLoader.instance.load_cmd_modules(),
                ModuleLoader.instance.load_auto_modules())



