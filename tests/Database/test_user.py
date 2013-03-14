#!/usr/bin/env python3
import unittest
import sqlite3

import os
import sys

lib_path = os.getcwd() + "/../../lib/backend"
sys.path.append( lib_path )
from database.user import User
from database.database import Database
from database.database import NoSuchTable

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

    def tearDown(self):
        self.connection.close()
        os.remove(self.gentest_config())
        os.remove(Database.db_file)

    def test_create_table(self):
        self.user.create_table()
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
        self.user.create_table()
        self.user.drop_table()
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'User';""")
        self.assertTrue(self.cursor.fetchone() == None, 
                "Database could not been droped")

    def test_getitem(self):
        self.user.create_table()
        self.assertEqual(self.user["c_id"], "Douglas")
        self.assertEqual(self.user["c_pubkey"], "pubkey")
        try:
            self.user["db_file"]
            self.assertTrue(False, "Was able to caught wrong attribute")
        except AttributeError:
            pass

    def test_get_attributes(self):
        self.user.create_table()
        attrs = self.user.get_attributes()
        self.assertTrue("c_id" in attrs)
        self.assertTrue("c_pubkey" in attrs)
        self.assertFalse("__doc__" in attrs)

    def test_save(self):
        with self.assertRaises(NoSuchTable):
            self.user.save()
        self.user.create_table()
        self.user.save()
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
        self.assertEqual(result[2], 'Douglas')
        self.assertEqual(result[3], 'pubkey')
        #updatecheck
        self.user.c_pubkey = "newpubkey"
        self.user.save()
        self.cursor.execute("""SELECT * FROM User
                        WHERE c_id = 'Douglas';""")
        res = self.cursor.fetchone()
        res = tuple(res)
        self.assertEqual(res[3], "newpubkey", 
                "Seems not to be updated correctly")
        self.assertEqual(res[2], "Douglas",
                "Seems not to be updated correctly")



    def test_get(self):
        self.user.create_table()
        self.user.save()
        results = User.get()
        self.assertEqual(self.user, results[0], "Unable to get all data")
        import datetime
        d = datetime.datetime.now() - datetime.timedelta(minutes=2)
        results = User.get(d)
        self.assertEqual(self.user, results[0], "Unable to get new data")

    def test_get_exacly(self):
        self.user.create_table()
        self.user.save()
        user = User.get_exacly(self.user.c_id)
        self.assertEqual(user, self.user, "Could not deserialize data")


if __name__ == "__main__":
    unittest.main()
