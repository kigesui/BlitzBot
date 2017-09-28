from configparser import ConfigParser


class BotConfig(object):
    class __BotConfig(ConfigParser):
        def __init__(self):
            init_file = "./configs.ini"
            super(BotConfig.__BotConfig, self).__init__()
            super(BotConfig.__BotConfig, self).read(init_file)

    instance = None

    """docstring for ClassName"""
    def __init__(self):
        if not BotConfig.instance:
            BotConfig.instance = BotConfig.__BotConfig()

    def get(self, *args):
        return BotConfig.instance.get(*args)
