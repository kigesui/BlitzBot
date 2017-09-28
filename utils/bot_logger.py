import logging
from time import localtime, strftime


class BotLogger:
    class __BotLogger():
        def __init__(self):
            logging.basicConfig()
            self.__logger = logging.getLogger("BotLogger")
            currtime = strftime("%Y%m%d-%H%M%S", localtime())
            hdlr = logging.FileHandler('./logs/bot_{}.log'.format(currtime))
            fmtr = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
            hdlr.setFormatter(fmtr)
            self.__logger.addHandler(hdlr)

            self.__logger.setLevel(1)

        def get_logger(self):
            return self.__logger

    instance = None

    def __init__(self):
        if not BotLogger.instance:
            BotLogger.instance = BotLogger.__BotLogger()
        self.__logger = BotLogger.instance.get_logger()

    def set_level(self, lvl):
        self.__logger.setLevel(lvl)

    # def log(self, level, msg, *args, **kwargs):
        # self.__logger.log(level, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.__logger.critical(msg, *args, **kwargs)
