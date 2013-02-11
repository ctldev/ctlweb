#!/usr/bin/env python3
import unittest
import sqlite3

import os
import sys

lib_path = os.getcwd() + "/../../lib/backend"
sys.path.append( lib_path )
from database.user import User
from database.database import Database

class UserTest(unittest.TestCase):
    """ Tests for user.py
    """
    def gentest_config(self):
        conffile = "test.conf"
        with open(conffile, "w") as file:
            file.write("""[Backend]
                        Hostname = localhost
                        User = foo
                        SSH-Port = 22
                        Database = test.db""")
        return conffile

    def setUp(self):
        Database(self.gentest_config())
        self.user = User("Douglas", "pubkey")
        self.connection = Database.db_connection
        self.cursor = self.connection.cursor()
        self.user.create_table()

    def tearDown(self):
        self.connection.close()
        os.remove(self.gentest_config())
        os.remove(Database.db_file)

    def test_create_table(self):
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'User';""")
        table_exists = False
        result = self.cursor.fetchone()
        self.assertFalse(result == None,
                "Table user could not been found")
        for i in result:
            if 'User' in i: table_exists = True
        self.assertTrue(table_exists)

    def test_drop_table(self):
        self.user.drop_table()
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'User';""")
        self.assertTrue(self.cursor.fetchone() == None, 
                "Database could not been droped")

    def test_getitem(self):
        self.assertEqual(self.user["c_id"], "Douglas")
        self.assertEqual(self.user["c_pubkey"], "pubkey")
        try:
            self.user["db_file"]
            self.assertTrue(False, "Was able to caught wrong attribute")
        except AttributeError:
            pass

    def test_get_attributes(self):
        attrs = self.user.get_attributes()
        self.assertTrue("c_id" in attrs)
        self.assertTrue("c_pubkey" in attrs)
        self.assertFalse("__doc__" in attrs)

    def test_save(self):
#       Restarting database connection
        self.connection.close()
        Database()
#       Try to read original data
        self.cursor = Database.db_connection.cursor()
        self.cursor.execute("""SELECT * FROM User
                WHERE c_id = 'Douglas';""")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result,
                "Couldn't read data from database")
        result = tuple(result)
        self.assertEqual(result[0], 'Douglas')
        self.assertEqaul(result[1], 'pubkey')


if __name__ == "__main__":
    unittest.main()