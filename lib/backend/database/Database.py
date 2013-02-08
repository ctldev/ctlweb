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
    db_connection = None

    def __init__(self, config_file='/etc/ctlweb.conf'):
        import configparser
        config = configparser.ConfigParser()
        config.read(config_file)

        if Database.db_file is None:
            Database.db_file = config['Backend']['Database']
        try:
            Database.db_connection.execute("""SELECT name from sqlite_master
                                                 LIMIT 1""")
            Database.db_connection.fetchone()
        except (sqlite3.ProgrammingError, AttributeError):
            Database.db_connection = sqlite3.connect(Database.db_file)

    def __getitem__(self, name):
        """ Grants access to all instance variables stored in db.
        """
        if not name.find("c_") == 0:
            raise AttributeError()
        return self.__getattribute__(name)

    def get_attributes(self):
        """ Returns all attributes which are stored in the database.
        """
        attributes = []
        for attr in dir(self):
            try:
                self[attr]
                attributes.append(attr)
            except AttributeError:
                pass
        return attributes

    def create_table(self):
        """ Creates a table for the class in which every instance object which
        stars with 'c_'. For example 'c_id'. This variable can be accessed with
        self["id"]

        NOT SUPPORTED YET!
        """
        pass

    def drop_table(self):
        """ Should remove the tables created by the class. Every child of
        database which stores is's own data should implement this function.

        NOT SUPPORTED YET!
        """
        pass

    def save(self):
        """ Saves object into database

        NOT SUPPORTED YET!
        """
        pass
