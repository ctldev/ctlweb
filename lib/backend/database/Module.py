#!/usr/bin/env python3
import output

class Module(Database):
    """ Is an module in the CTL-Database
    """
    def __init__(self, name, exe, ci):
        """ Documentation text is not supported, because it could be to big.
        """
        super()
        self.c_id = name
        self.c_exe = exe
        self.c_ci = ci

    def create_table(self):
        cursor = Database.db_connection.cursor()
        create_table = """CREATE TABLE Module (
                            id TEXT PRIMARY,
                            exe TEXT,
                            ci TEXT,
                            );
                           """ 
        cursor.execute(create_table)
        cursor.commit()

    def drop_table():
        """ Be carefull with it! Could destroy important data
        """
        cursor = Database.db_connection.cursor()
        cursor.execute("DROP TABLE module;")
        cursor.commit()

