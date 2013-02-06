#!/usr/bin/env python3
from .Database import Database
import sqlite3

class User(Database):
    """ An registered user
    """

    def __init__(self, name, pubkey):
        super()
        self.c_id = name
        self.c_pubkey = pubkey

    def create_table(self):
        cursor = Database.db_connection.cursor()
        create_table = """CREATE TABLE User (
                            c_id TEXT PRIMARY KEY,
                            c_pubkey TEXT
                            );
                            """
        cursor.execute(create_table)
        Database.db_connection.commit()

    def drop_table(self):
        """ Be carefull with it! Could destroy important data
        """
        cursor = Database.db_connection.cursor()
        cursor.execute("DROP TABLE user;")
        Database.db_connection.commit()

