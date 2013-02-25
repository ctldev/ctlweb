#!/usr/bin/env python3
import unittest
import sqlite3
import os
import sys

lib_path = os.getcwd() + "/../../lib/backend"
sys.path.append( lib_path )
from database.component import Component
from database.database import Database

class TestComponent(unittest.TestCase):
    """ Testing of module.py
    """
    def setUp(self):
        """ Establishes database connection
        """
        Database.db_file = "test.db" # DB File for Testcase without config
#       Instance objects
        self.comp = Component("name","/path/to/exe","/path/to/ci")
        self.connection = Database.db_connection
        self.cursor = self.connection.cursor()
        self.comp.create_table()

    def tearDown(self):
        """ Closes database connection and removes database from disk
        """
        Database.db_connection.close()
        os.remove(Database.db_file)

    def test_create_table(self):
        self.assertIsNotNone(self.connection, 
                "Database isn't correctly initialized")
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'Component';""")
        table_exists = False
        for i in self.cursor.fetchone():
            if 'Component' in i: table_exists = True
        self.assertTrue(table_exists)

    def test_drop_table(self):
        try:
            self.comp.drop_table()
        except sqlite3.OperationalError:
            self.assertFalse(True, "Error while table drop")
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'Component';""")
        self.assertIsNone(self.cursor.fetchone())

    def test_getitem(self):
        """ Tests if access to instance objects with names like c_ are
        possible. Errors or Fails need to be fixed in class Database.
        """
        self.assertEqual(self.comp["c_id"], "name" )
        self.assertEqual(self.comp["c_exe"], "/path/to/exe" )
        self.assertEqual(self.comp["c_ci"], "/path/to/ci" )
        try:
            self.comp["db_file"]
            self.assertTrue(false, "Got access to wrong variable")
        except AttributeError:
            pass

    def test_get_attributes(self):
        """ Tests if all instance objects are found by get_attributes(). Errors
        or Fails need to be fixed in class Database.
        """
        attrs = self.comp.get_attributes()
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
        self.comp.save()
#       connection restart
        self.connection.close()
        Database()
#       test if data still present
        cursor = self.comp.db_connection.cursor()
        cursor.execute("SELECT * FROM Component;")
        res = cursor.fetchone()
        self.assertIsNotNone(res, "Could not read test data from db.")
        res = tuple(res)
        self.assertEqual(res[0], "name", "Got unexpected data")
        self.assertEqual(res[1], "/path/to/exe", "Got unexpected data")
        self.assertEqual(res[2], "/path/to/ci", "Got unexpected data")

    def test_conform(self):
        """ Test for sqlite3 representation
        """
        repr = self.comp.__conform__(sqlite3.PrepareProtocol)
        self.assertEqual(repr, "c_id=name;c_exe=/path/to/exe;c_ci=/path/to/ci",
                msg="Error in generation of representation")

    def test_convert(self):
        """ Tests if a __conform__ representation could be successfully
        rebuild.
        """
        repr =  "c_id=name;c_exe=/path/to/exe;c_ci=/path/to/ci"
        comp = Component.convert(repr)
        self.assertEqual(comp, self.comp)

    def test_get(self):
        self.comp.save()
        comps = Component.get()
        self.assertEquals(comps[0], self.comp, "Could not deserialize data")

    def test_get_exacly(self):
        self.comp.save()
        comp = Component.get_exacly(self.comp.c_id)
        self.assertEquals(comp, self.comp, "Could not deserialize data")

if __name__ == '__main__':
    unittest.main()
