#!/usr/bin/env python3
import unittest
import sys
import os
import sqlite3

test_root = os.getcwd() + "/../.."
sys.path.append( test_root + "/lib/backend/")
from database.database import Database

class DatabaseTest(unittest.TestCase):

    def setUp(self):
        Database.db_file = ":memory:"
        self.db = Database(test_root+"/etc/ctlweb.conf")

    def test_creation(self):
        """ Basic test for creating Database object
        """
#       DB basics are initialized?
        self.assertIsNotNone(Database.db_file)
        self.assertIsNotNone(Database.db_connection)
        self.assertIsInstance(Database.db_connection, sqlite3.Connection)

if __name__ == '__main__':
    unittest.main()
