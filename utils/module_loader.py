# from utils.bot_logger import BotLogger

# modules import
from modules.ping.ping import PingModule
from modules.halls.halls import HallsModule


class ModuleLoader:
    class __ModuleLoader():
        def __init__(self):
            pass

        def load_auto_modules(self):
            """ Auto modules execute command without bot prefix """
            auto_modules = []
            return auto_modules

        def load_cmd_modules(self):
            """ Command modules execute command after bot prefix """
            cmd_modules = []
            cmd_modules.append(PingModule())
            # cmd_modules.append(HallsModule())
            return cmd_modules

    instance = None

    def __init__(self):
        if not ModuleLoader.instance:
            ModuleLoader.instance = ModuleLoader.__ModuleLoader()

    def load_all_modules(self):
        return (ModuleLoader.instance.load_cmd_modules(),
                ModuleLoader.instance.load_auto_modules())



