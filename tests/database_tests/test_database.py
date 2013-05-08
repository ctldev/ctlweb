#!/usr/bin/env python3
import unittest
import sys
import os
import sqlite3

from database.database import Database
from database.web import Web
from database.user import User

class DatabaseTest(unittest.TestCase):

    def _gentest_config(self):
        conffile = "test.conf"
        with open(conffile, "w") as file:
            file.write("""[Backend]
                        Hostname = localhost
                        User = foo
                        SSH-Port = 22
                        Database = test.db
                        Manifest_store = /dev/null""")
        return conffile

    def setUp(self):
        Database.db_file = ":memory:"
        self.db = Database(self._gentest_config())

    def test_creation(self):
        """ Basic test for creating Database object
        """
#       DB basics are initialized?
        self.assertIsNotNone(Database.db_file)
        self.assertIsNotNone(Database.db_connection)
        self.assertIsInstance(Database.db_connection, sqlite3.Connection)

    def test_eq(self):
        """ Equals method
        """
        web1 = Web("test","test")
        web2 = Web("test","test")
        web3 = Web("na","ne")
        user = User("test","test")
        self.assertEqual(web1, web2)
        self.assertNotEqual(web1, web3)
        self.assertNotEqual(web1, user)
        self.assertNotEqual(web1, None)

if __name__ == '__main__':
    unittest.main()
