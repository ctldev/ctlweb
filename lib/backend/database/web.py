#!/usr/bin/env python3
import sqlite3
from .database import Database

class Web(Database):
    """ An registerd ctlweb instance
    """

    def __init__(self, url, pubkey):
        super().__init__()
        self.c_id = url
        self.c_pubkey = pubkey

    def create_table(self):
        cursor = Database.db_connection.cursor()
        create_table = """CREATE TABLE Web (
                            id TEXT PRIMARY KEY,
                            pubkey TEXT,
                            adapter TEXT
                            );
                            """
        cursor.execute(create_table)
        Database.db_connection.commit()

    def drop_table(self):
        """ Be carefull with it! Could destroy important data
        """
        cursor = Database.db_connection.cursor()
        cursor.execute("DROP TABLE web;")
        Database.db_connection.commit()

