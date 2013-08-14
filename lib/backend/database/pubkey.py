#!/usr/bin/env python3
from .database import Database
from database.database import NoSuchTable
import sqlite3
from util import Log

class Pubkey(Database):
    """ Is a public userkey in the CTL-Database
    """
    authorized_keys_file = None

    def __init__(self, key, access):
        """ Should not be used, use Component.create() instead.
        """
        super().__init__()
        self.c_key = key
        self.f_Access_access = int(access.c_pk)
        self.c_id = -1
        self.c_referenced_class = access.__class__.__name__

        import configparser
        from os import path
        reader = configparser.ConfigParser()
        reader.read(Database.config)
        if Pubkey.authorized_keys_file:
            return
        try:
            Pubkey.authorized_keys_file = reader['Backend', 'authorized_keys']
        except KeyError:
            home = path.expanduser('~')
            Pubkey.authorized_keys_file = path.join(home, '.ssh',
                                                    'authorized_keys')

    def save(self):
        super().save()
        if not self.c_id == self.c_pk:
            self.c_id = self.c_pk
            self.save()

    @classmethod
    def create(cls, attr):
        """ attr is expected to be a dict with the following keys:
            * c_id: will be auto-incremented with the pk
            * f_Access_access: the access-type class the key belongs to
            * c_key: the userkey
        """
        key = cls(attr["c_key"], attr['f_Access_access'])
        key._write_key()
        return key

    def remove(self):
        """ Remove component with given name.
        
        Returns True if the component successfully removed.
        """
        Log.debug("Pubkey.remove(): removing")
        self._remove_key()
        super().remove()
        return True

    @classmethod
    def add(cls, key, access):
        """ A given key will be added to the local database, referencing the
        given Access-Instance.

        returns newly created object
        """
        from os import path
        Log.debug("add(package): adding package to local database")
        # Create Database entry
        data = {'c_key': key, 'f_Access_access': access,}
        pubkey = cls.create(data)
        try:
            pubkey.save()
        except NoSuchTable:
            pubkey.create_table().save()
        return pubkey

    @staticmethod
    def get_access_keys(access):
        """ returns all keys referencing the specified Access-Instance
        """
        data = []
        sql = 'SELECT c_pk, adapter FROM Pubkey WHERE f_Access_access = ?'
        cursor = Database.db_connection.cursor()
        Log.debug('Pubkey.get_access_keys(): '\
                  + 'Requesting Pubkeys with access c_pk = %s' % access.c_pk)
        Log.debug('Pubkey.get_access_keys(): executing query: ' + sql)
        try:
            cursor.execute(sql, (str(access.c_pk),))
            for key in cursor.fetchall():
                data.append(Pubkey.convert(key))
        except sqlite3.OperationalError:
            cursor.execute("""SELECT name FROM sqlite_master
                              WHERE name = 'Pubkey';""")
            result = cursor.fetchone()
            if result:
                raise Database.GeneralDatabaseError()
            Pubkey('', access).create_table()
        Log.debug('Pubkey.get_access_keys(): found %s elements' % len(data))
        return data

    def _keyline(self):
        """Return an authorized_keys compatible line with access definitions.
        """
        return ''

    def _write_key(self):
        """ Adds the own access with the _keyine() to authorized_keys
        """
        with open(Pubkey.authorized_keys_file, 'a') as authorized_key_file:
            authorized_key_file.write(self._keyline())

    def _remove_key(self):
        removal_lins = []
        new_authorized_keys = "%s.new" % Pubkey.authorized_keys_file
        # Transfer the good lines
        with open(Pubkey.authorized_keys_file, 'r') as old_auth:
            with open(new_authorized_keys, 'w') as new_auth:
                for line in old_auth:
                    if line == self._keyline(): # line to be removed
                        continue
                    new_auth.write(line)
        # switch files
        import os
        os.rename(Pubkey.authorized_keys_file, "%s~" %
                Pubkey.authorized_keys_file)
        os.rename(new_authorized_keys, Pubkey.authorized_keys_file)
