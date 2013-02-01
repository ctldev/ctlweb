#!/usr/bin/env python3

class User(Database):
    """ An registered user
    """

    def __init__(self, name, pubkey):
        super()
        self.c_id = name
        self.c_pubkey = pubkey

    def create_table(self):
        cursor = Database.db_connection.cursor()
        create_table = """CREATE TABLE user (
                            id TEXT PRIMARY,
                            pubkey TEXT,
                            );
                            """
        cursor.execute(create_table)
        cursor.commit()

    def drop_table():
        """ Be carefull with it! Could destroy important data
        """
        cursor = Database.db_connection.cursor()
        cursor.execute("DROP TABLE user;")
        cursor.commit()

