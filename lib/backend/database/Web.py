#!/usr/bin/env python3

class Web(Database):
    """ An registerd ctlweb instance
    """

    def __init__(self, url, pubkey):
        super()
        self.c_id = url
        self.c_pubkey = pubkey

    def create_table(self):
        cursor = Database.db_connection.cursor()
        create_table = """CREATE TABLE web (
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
        cursor.execute("DROP TABLE web;")
        cursor.commit()

