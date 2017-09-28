from utils.bot_logger import BotLogger

# modules import
from modules.ping.ping import PingModule


class ModuleLoader:
    class __ModuleLoader():
        def __init__(self):
            pass

        def load_modules(self):
            BotLogger().debug("Loading Modules")
            all_modules = []
            all_modules.append(PingModule())
            return all_modules

    instance = None

    def __init__(self):
        if not ModuleLoader.instance:
            ModuleLoader.instance = ModuleLoader.__ModuleLoader()

    def load_modules(self):
        return ModuleLoader.instance.load_modules()



