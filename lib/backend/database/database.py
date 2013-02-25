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
        # Creationtime of object
        c_creation = None


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
        """
        cursor = self.db_connection.cursor()
        sql = "CREATE TABLE "
        sql += self.__name__
        sql += """ (
                date DATE,
                adapter TEXT"""
        for i in self.get_attributes():
            sql += ", "+i 
        sql += ");"
        cursor.execute(sql)
        self.db_connection.commit()

    def drop_table(self):
        """ Should remove the tables created by the class. Every child of
        database which stores is's own data should implement this function.
        """
        cursor = self.db_connection.cursor()
        sql = "DROP TABLE "
        sql += self.__name__
        cursor.execute(sql)
        self.db_connection.commit()

    def save(self):
        """ Saves object into database

        NOT SUPPORTED YET!
        """
        
        cursor = Database.db_connection.cursor()
        pdb.set_trace()
        attributes = self.get_attributes()

        table = self.__class__.__name__
        targetcolumns = []  
        values = [] 
        updatetargetvalues = []
        for a in attributes:
            if a == attributes[-1]:
                targetcolumns.append(a)
                values.append(self[a])
                updatetargetvalues.append(a)
                updatetargetvalues.append("=")
                updatetargetvalues.append(self[a])
            else: 
                targetcolumns.append(a)
                targetcolumns.append(",")
                values.append(self[a])
                updatetargetvalues.append(a)
                updatetargetvalues.append("=")
                updatetargetvalues.append(self[a])
                updatetargetvalues.append(",")
        stringtargetcolumns = "".join(targetcolumns)
        stringvalues = "".join(values)
        sstringupdatetargetvalues = "".join(updatetargetvalues)
        parameter = {"table" : table, "columns" : stringtargetcolumns, 
                "values" : stringvalues, "set" : stringupdatetargetvalues}
        print(parameter)
        try:
            sql = """INSERT INTO :table (:columns) 
                    VALUES (:values)"""
            cursor.execute(sql,parameter)
            Database.db_connection.commit()
        except SQLiteException:
            exceptionparameter = (targetcolumns[0], values[0])
            sql = "UPDATE :table SET :set WHERE ? = ?"
            cursor.execute(sql,parameter,exceptionparameter)
            Database.db_connection.commit()

    def __conform__(self,protocol):
        """ For creating an generall repräsentation of the class. The
        representation looks like the following:
         "c_id=2;c_pubkey=publickey"
         TODO: escaping the strings
        """
        if protocol is sqlite3.PrepareProtocol:
            attributes = self.get_attributes()
            repr = ""
            first = True
            for attr in attributes:
                # Works only if all attributes are simple types like 
                # string, int,...
                if first:
                    repr = attr + "=" + self[attr]
                    first = False
                else:
                    repr = attr + "=" + self[attr] + ";" + repr
            return repr

    @classmethod
    def convert(cls, s):
        """ Returns an object build out of the string s. This function is used
        by sqlite3
         TODO: registration in sqlite3
         TODO: escaping the strings
        """
        attribute_box = {}
        for attr in s.split(";"):
            key, val = attr.split("=")
            attribute_box[key] = val
        return cls.create(attribute_box)

    def __eq__(self, db):
        """ Objects are equal if attributes of get_attribute() are equal.
        """
        if not isinstance(db, self.__class__):
            return False
        set1 = dir(self)
        set2 = dir(db)
        if set1 != set2:
            return False
        eq = True
        for i in self.get_attributes():
            try:
                eq &= db[i] == self[i]
            except AttributeError:
                return False
        return eq
    
    @property
    def __name__(self):
        """ Provides that the name of the class is callable
        """
        return self.__class__.__name__

    @classmethod
    def get(cls, time_since):
        """ Returns a tuple of objects stored in the database.
        """
        import re
        statement = """SELECT adapter FROM ?
                WHERE date BETWEEN ? AND date('now')"""
        if not re.search(r'^[1-2]\d{3}-[0-1]?\d-[0-3]?\d$', time_since):
            raise ValueError()
        cursor = db_connection.cursor()
        cursor.execute(statement, time_since)
        result_set = []
        for row in cursor.fetchall():
            result_set.append(cls.convert(row))

    @classmethod
    def get_excat(cls, name):
        """ Returns exacly one object with the given (unique) name.
        """
        pass
