#!/usr/bin/env python3
import unittest
import sqlite3
import os
import sys

lib_path = os.getcwd() + "/../../lib/backend"
sys.path.append( lib_path )
from database.Module import Module
from database.Database import Database

class TestModule(unittest.TestCase):
    """ Testing of module.py
    """
    def setUp(self):
        """ Establishes database connection
        """
        Database.db_file = "test.db" # DB File for Testcase without config
#       Instance objects
        self.mod = Module("name","/path/to/exe","/path/to/ci")
        self.connection = Database.db_connection
        self.cursor = self.connection.cursor()
        self.mod.create_table()

    def tearDown(self):
        """ Closes database connection and removes database from disk
        """
        Database.db_connection.close()
        os.remove(Database.db_file)

    def test_create_table(self):
        self.assertIsNotNone(self.connection, 
                "Database isn't correctly initialized")
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'Module';""")
        table_exists = False
        for i in self.cursor.fetchone():
            if 'Module' in i: table_exists = True
        self.assertTrue(table_exists)

    def test_drop_table(self):
        self.mod.drop_table()
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'Module';""")
        self.assertIsNone(self.cursor.fetchone())

    def test_getitem(self):
        """ Tests if access to instance objects with names like c_ are
        possible. Errors or Fails need to be fixed in class Database.
        """
        self.assertEqual(self.mod["c_id"], "name" )
        self.assertEqual(self.mod["c_exe"], "/path/to/exe" )
        self.assertEqual(self.mod["c_ci"], "/path/to/ci" )
        try:
            self.mod["db_file"]
            self.assertTrue(false, "Got access to wrong variable")
        except AttributeError:
            pass

    def test_get_attributes(self):
        """ Tests if all instance objects are found by get_attributes(). Errors
        or Fails need to be fixed in class Database.
        """
        attrs = self.mod.get_attributes()
        self.assertTrue(attrs, msg="Got no attributes")
        self.assertTrue("c_id" in attrs , 
                msg="Caught the following attributes: %s"%attrs)
        self.assertTrue("c_exe" in attrs ,
                msg="Caught the following attributes: %s" % attrs)
        self.assertTrue("c_ci" in attrs ,
                msg="Caught the following attributes: %s" % attrs)
        self.assertFalse("__doc__" in attrs,
                msg="Caught __doc__ attribute which is wrong")

    def test_save(self):
        """ Checks if data can be made persistent in the database
        """
        self.mod.save()
#       connection restart
        self.connection.close()
        Database()
#       test if data still present
        cursor = self.mod.db_connection.cursor()
        cursor.execute("SELECT * FROM Module;")
        res = cursor.fetchone()
        self.assertIsNotNone(res, "Could not read test data from db.")
        res = tuple(res)
        self.assertEqual(res[0], "name", "Got unexpected data")
        self.assertEqual(res[1], "/path/to/exe", "Got unexpected data")
        self.assertEqual(res[2], "/path/to/ci", "Got unexpected data")


if __name__ == '__main__':
    unittest.main()
