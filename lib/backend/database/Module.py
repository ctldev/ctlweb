#!/usr/bin/env python3
import sqlite3
from .Database import Database

class Module(Database):
    """ Is an module in the CTL-Database
    """
    def __init__(self, name, exe, ci):
        """ Documentation text is not supported, because it could be to big.
        """
        super().__init__()
        self.c_id = name
        self.c_exe = exe
        self.c_ci = ci

    def create_table(self):
        connection = Database.db_connection
        cursor = Database.db_connection.cursor()
        create_table = """CREATE TABLE Module (
                            id TEXT PRIMARY KEY,
                            exe TEXT,
                            ci TEXT
                            );
                           """ 
        cursor.execute(create_table)
        connection.commit()

    def drop_table(self):
        """ Be carefull with it! Could destroy important data
        """
        cursor = Database.db_connection.cursor()
        cursor.execute("DROP TABLE module;")
        Database.db_connection.commit()

