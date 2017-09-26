from configparser import ConfigParser


class BotConfig(ConfigParser):
    def __init__(self, *args):
        init_file = "./configs.ini"
        super(BotConfig, self).__init__()
        super(BotConfig, self).read(init_file)



