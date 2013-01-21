#!/usr/bin/env python3
import sqlite3

class Database:
    """ Every class derived from Database gets it's own table in the database.
    The columns are defined by the instance attributes starting with 'c_'. Only
    attributes in the following type can be stored:

        * unicode string
        * int
    """
    db_file = None

    def __init__(self, config_file='/etc/ctlweb.conf'):
        import configparser
        config = configparser.ConfigParser()
        config.read(config_file)

        if Database.db_file is None:
            Database.db_file = config['Backend']['Database']

    def __getitem__(self, name):
        """ Grants access to all instance variables stored in db.
        """
        return self.__getattribute__("c_"+name)

    def create_table():
        """ Creates a table for the class in which every instance object which
        stars with 'c_'. For example 'c_id'. This variable can be accessed with
        self.["id"]
        """
        pass

    def remove_table():
        """ Should remove the tables created by the class. Every child of
        database which stores is's own data should implement this function.
        """
        pass
