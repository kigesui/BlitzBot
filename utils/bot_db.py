import sqlite3
import os.path

# from utils.bot_logger import BotLogger


class BotDB(object):
    """ Adaptor to connect to SQLite
    """
    class __BotDB(object):
        def __init__(self):
            self.db_filename = "./data/blitzbot.db"
            # check if file exists
            if not os.path.isfile(self.db_filename):
                self.__create_db_file()

        def __create_db_file(self):
            cxn = sqlite3.connect(self.db_filename)
            cxn.commit()
            cxn.close()
            return

        def __connect(self):
            return sqlite3.connect(self.db_filename)

    """ singleton """
    instance = None

    """ init for singleton """
    def __init__(self):
        if not BotDB.instance:
            BotDB.instance = BotDB.__BotDB()

    def get_connection(self):
        return BotDB.instance.__connect()
