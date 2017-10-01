import sqlite3
import os.path

from utils.bot_logger import BotLogger


class BotDB(object):
    class __BotDB(object):
        def __init__(self):
            self.db_file = "./data/blitzbot.db"
            # check if file exists
            if not os.path.isfile(self.db_file):
                self.__create_tables()

        def __create_tables(self):
            # create the file
            cxn = sqlite3.connect(self.db_file)
            # make cursor
            curs = cxn.cursor()

            # create hall of poop
            # curs.execute('''DROP TABLE IF EXISTS  `hallPoop`''')
            curs.execute('''CREATE TABLE hallPoop (
                              user_id text NOT NULL,
                              amount integer,
                              PRIMARY KEY (user_id)
                            );''')

            # create badge
            curs.execute('''CREATE TABLE badges (
                              badge_id text NOT NULL,
                              badge_emoji text,
                              PRIMARY KEY (badge_id)
                            );''')

            # create user-badges
            curs.execute('''CREATE TABLE userBadges (
                              user_id text NOT NULL,
                              badge_id text NOT NULL,
                              amount integer,
                              PRIMARY KEY (user_id, badge_id),
                              FOREIGN KEY (badge_id)
                                REFERENCES badges (badge_id)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE
                            );''')

            # save and close cursor
            cxn.commit()
            cxn.close()
            return

        """
        giant switch function
        """
        def execute(self, *args):
            if args[1] == "hallPoop":
                if args[0] == "get":
                    return self.__get_hall_poop()
                elif args[0] == "save":
                    return self.__save_hall_poop(args[2])
                else:
                    return None
            return None

        """
        individial sql queries starts here
        """
        def __get_hall_poop(self):
            BotLogger().debug("getting poop hall")
            # connect and get cursor
            cxn = sqlite3.connect(self.db_file)
            curs = cxn.cursor()
            # sql query
            ret_val = curs.execute("""SELECT *
                                        FROM hallPoop
                                        ORDER BY amount
                                   """)
            # make ret_val a dict
            ret_dict = {}
            for row in ret_val:
                ret_dict[row[0]] = row[1]
            # close
            cxn.close()
            return ret_dict

        def __save_hall_poop(self, new_table):
            BotLogger().debug("saving poop hall")
            # connect and get cursor
            cxn = sqlite3.connect(self.db_file)
            curs = cxn.cursor()
            # drop table
            curs.execute("""DELETE FROM hallPoop""")
            # dict to query
            for user_id, amount in new_table.items():
                curs.execute("""INSERT INTO hallPoop
                                  VALUES (?, ?)
                             """, (user_id, amount))
            # commit and close connection
            cxn.commit()
            cxn.close()
            return

    """ singleton """
    instance = None

    """ init for singleton """
    def __init__(self):
        if not BotDB.instance:
            BotDB.instance = BotDB.__BotDB()

    """ load table by executing query """
    def get(self, table_id):
        return BotDB.instance.execute("get", table_id)

    def save(self, table_id, new_table):
        return BotDB.instance.execute("save", table_id, new_table)
