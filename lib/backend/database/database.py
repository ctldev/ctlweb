#!/usr/bin/env python3
import sqlite3
import sys
from util import Log
from util.settings import DEFAULT_CONFIG


class Database:
    """ Every class derived from Database get its own table in the database.
    The columns are defined by the instance attributes starting with 'c_'. Only
    attributes in the following type can be stored:

        * unicode string
        * int
    Moreover, Foreign Keys can be stored by the prefix
    'f_<referencedClassName>_'.
    """
    db_file = None
    db_connection = None
    store = None
    config = None
    """ The manifest store """

    def __init__(self, config_file=DEFAULT_CONFIG):
        import configparser
        reader = configparser.ConfigParser()
        reader.read(config_file)
        self.c_pk = -1
        if not Database.config:
            Database.config = config_file  # share config file with others

        if Database.store is None:
            try:
                Database.store = reader.get('Backend','Manifest_store')
            except configparser.Error:
                Log.critical("""Your Config-File seems to be malformated! Check
                your Config-File and try again!""")
                sys.exit(1)
        if Database.db_file is None:
            try:
                Database.db_file = reader.get('Backend','Database')
                import os
                if os.path.isdir( Database.db_file ):
                    Log.critical("Database(): Database is directory!")
                    sys.exit(1)

            except configparser.Error:
                Log.critical("""Your Config-File seems to be malformated! Check
                your Config-File and try again!""")
                sys.exit(1)
        try: # Check if connection is active
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
        import re
        format_foreign_key = 'f_(?P<classname>.+?)_.+'
        format_column = 'c_'
        if not re.search('^(%s|%s)' % (format_foreign_key, format_column),
                         name):
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

    @classmethod
    def get(cls, time_since=None):
        """ Returns a list of objects stored in the database.
        Optional Parameter time_since is instance of datetime.datetime and
        represents the oldest object to be found by get. Default searches for
        every object stored in the database.
        """
        # FIXME should use the get_exactly for easy maintenance; skipped due to
        #       motivational problems
        from datetime import datetime
        sql = "SELECT c_pk, adapter FROM " + cls.__name__ + """
                WHERE date >= ?"""
        values = []
        if not time_since:
            Log.debug("Database.get(): Get all objects of %s" % cls.__name__)
            sql = "SELECT c_pk, adapter FROM " + cls.__name__
        elif isinstance(time_since, datetime):
            Log.debug("Database.get(): Get %s newer than %s" %
                    (cls.__name__, time_since))
            time_since = time_since.strftime("%s")
            values.append(time_since)
        else:
            Log.debug("Wrong dateformat caught in %s.get()" % cls.__name__)
            raise ValueError()
        cursor = Database.db_connection.cursor()
        try:
            cursor.execute(sql, values)
        except sqlite3.IntegrityError:
            return None
        except sqlite3.OperationalError:
            raise NoSuchTable()
        result_set = []
        for row in cursor.fetchall():
            result_set.append(cls.convert(row))
        return result_set

    @classmethod
    def get_exactly(cls, name, field='c_id'):
        """ Returns exactly one object with the given (unique) name.
        If no object with the given name was found, a InstanceNotFoundError is
        raised.
        """
        sql = 'SELECT c_pk, adapter FROM ' + cls.__name__ + ' WHERE '
        sql += '%s = ?' % field
        cursor = Database.db_connection.cursor()
        Log.debug("Database.get_exactly(): Requesting %s with %s = %s" \
                % (cls.__name__, field, name))
        Log.debug("Database.get_exactly(): executing query: " + sql)
        try:
            cursor.execute(sql, (name, ))
        except sqlite3.OperationalError:
            raise NoSuchTable()
        try:
            return cls.convert(cursor.fetchone())
        except TypeError: # Object was not in database
            raise InstanceNotFoundError()

    def create_table(self):
        """ Creates a table for the class in which every instance object which
        starts with 'c_'. For example 'c_id'. This variable can be accessed with
        self["c_id"]

        returns self
        """
        import re
        Log.debug("Creating Table for %s" % self.__name__)
        cursor = self.db_connection.cursor()
        sql = "CREATE TABLE "
        sql += self.__name__
        sql += """ (
                c_pk INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                adapter TEXT""" 
        attrs = self.get_attributes()
        if not 'c_id' in attrs:
            raise AttributeError('c_id not defined')
        for i in attrs:
            if i == 'c_pk':
                continue
            if i == "c_id":
                sql += ", %s UNIQUE" % i
            elif re.search('^f_(?P<classname>.+?)_.+', i):
                class_match = re.match('^f_(?P<classname>.+?)_.+', i)
                referenced_class = class_match.groupdict()['classname']
                sql += ', %s REFERENCES %s (c_pk)' % (i, referenced_class)
            else:
                sql += ", %s" % i
        sql += ");"
        Log.debug('Creating table, executing query: ' + sql)
        cursor.execute(sql)
        self.db_connection.commit()
        return self

    def drop_table(self):
        """ Should remove the tables created by the class. Every child of
        database which stores its own data should implement this function.
        """
        Log.debug("Dropping Table %s" % self.__name__)
        cursor = self.db_connection.cursor()
        sql = "DROP TABLE "
        sql += self.__name__
        cursor.execute(sql)
        self.db_connection.commit()

    def remove(self):
        """ Removes rows on the basis of the id
        """
        Log.debug('Removing object from database.')
        cursor = Database.db_connection.cursor()
        table = self.__name__
        sql = "DELETE FROM " +table+ """
                WHERE c_id = """ "'%s'" """
                """ % self["c_id"]
        cursor.execute(sql)
        Database.db_connection.commit()


    def save(self):
        """ Saves object into database
        """
        Log.debug('Saving object to database')
        cursor = Database.db_connection.cursor()
        attributes = self.get_attributes()
        table = self.__name__
        row_patterns = ""
        header = ' (date, adapter'
        values = {
                'adapter' : self,
                }
        for i in attributes:
            if i == 'c_pk':
                continue
            header += ', ' + i
            row_patterns += ", :" + i
            values[i] = self[i]
        else:
            row_patterns += ")"
            header += ')'
        try:
            if not self.c_pk == -1:
                raise sqlite3.IntegrityError()
            sql = "INSERT INTO " + table + header + """
                    VALUES
                    (strftime('%s','now'), :adapter """ + row_patterns
            Log.debug("Database.save(): %s as insert with %s as dict" %
                      (sql, values))
            cursor.execute(sql,values)
            Database.db_connection.commit()
            self.c_pk = cursor.lastrowid
        except sqlite3.IntegrityError:
            sql = ""
            for i in attributes:
                if i == 'c_pk':
                    continue
                sql += ", "+i
                sql += " = '"+str(self[i])+"'"
            values['c_pk'] = self.c_pk
            sql = "UPDATE " + table + """
                    SET
                    date = (strftime('%s', 'now')),
                    c_id = :c_id,
                    adapter = :adapter """ +sql+ """
                    WHERE c_pk = :c_pk """
            Log.debug("Database.save(): %s as update query with %s as dict" %
                      (sql, values))
            cursor.execute(sql,values)
            Database.db_connection.commit()
        except sqlite3.OperationalError:
            raise NoSuchTable()


    def __conform__(self,protocol):
        """ For creating an general representation of the class. The
        representation looks like the following:
         "c_id=2;c_pubkey=publickey"
         TODO: escaping the strings
        """
        if protocol is sqlite3.PrepareProtocol:
            attributes = self.get_attributes()
            repr = ""
            first = True
            for attr in attributes:
                if attr == 'c_pk':
                    continue
                # Works only if all attributes are simple types like
                # string, int,...
                if first:
                    repr = attr + "=" + str(self[attr])
                    first = False
                else:
                    repr = attr + "=" + str(self[attr]) + ";" + repr
            return repr
        elif isinstance(protocol, type(self)):
            attributes = self.get_attributes()
            repr = ""
            first = True
            for attr in attributes:
                if first:
                    repr = "{'%s': %s" % (attr, self[attr])
                    first = False
                else:
                    repr = "%s, '%s': %s" % (repr, attr, self[attr])
            else:
                repr += "}"
            return repr

    @classmethod
    def convert(cls, s):
        """ Returns an object built out of the string s. This function is used
        by sqlite3
        """
        Log.debug("Building %s object" % cls.__name__)
        attribute_box = {}
        attribute_box['c_pk'] = s[0]
        import re
        attrs = s[1].split(';')
        for attr in sorted(attrs):
            key, val = attr.split("=")
            if re.search('^f_(?P<classname>.+?)_.+', key):
                class_name = attribute_box['c_referenced_class']
                exec('from .%s import %s' % (class_name.lower(), class_name))
                exec('attribute_box[key] = ' + class_name \
                     + ".get_exactly(val, 'c_pk')")
                continue
            attribute_box[key] = val
        Log.debug('Got following attributes: ' + str(attribute_box))
        instance = cls.create(attribute_box)
        instance.c_pk = s[0]
        return instance

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

    def __str__(self):
        attr = self.get_attributes()
        return "%s.create(%s)" % (self.__name__, self.__conform__(self))

class InstanceNotFoundError(ValueError):
    pass

class NoSuchTable(sqlite3.OperationalError):
    pass

class DatabaseNotFound(sqlite3.OperationalError):
    pass

class GeneralDatabaseError(sqlite3.OperationalError):
    pass
