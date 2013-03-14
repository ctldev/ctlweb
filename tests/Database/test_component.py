#!/usr/bin/env python3
import unittest
import sqlite3
import os
import sys

lib_path = os.getcwd() + "/../../lib/backend"
sys.path.append( lib_path )
from database.component import Component
from database.database import Database
from database.database import NoSuchTable
from util import Log

class TestComponent(unittest.TestCase):
    """ Testing of module.py
    """
    def setUp(self):
        """ Establishes database connection
        """
        Database.db_file = "test.db" # DB File for Testcase without config
        Log.streamoutput(5)
#       Instance objects
        self.comp = Component("name","/path/to/exe","/path/to/ci")
        self.connection = Database.db_connection
        self.cursor = self.connection.cursor()

    def tearDown(self):
        """ Closes database connection and removes database from disk
        """
        Database.db_connection.close()
        os.remove(Database.db_file)

    def test_create_table(self):
        self.comp.create_table()
        self.assertIsNotNone(self.connection, 
                "Database isn't correctly initialized")
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'Component';""")
        table_exists = False
        for i in self.cursor.fetchone():
            if 'Component' in i: table_exists = True
        self.assertTrue(table_exists)

    def test_drop_table(self):
        self.comp.create_table()
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
        self.comp.create_table()
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
        self.comp.create_table()
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
        with self.assertRaises(NoSuchTable):
            self.comp.save()
        self.comp.create_table()
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
        self.assertEqual(res[4], "name", "Got unexpected data")
        self.assertEqual(res[3], "/path/to/exe", "Got unexpected data")
        self.assertEqual(res[2], "/path/to/ci", "Got unexpected data")
        #updatecheck
        self.comp.c_exe = "updatedexe"
        self.comp.save()
        cursor.execute("SELECT * FROM Component;")
        res = cursor.fetchone()
        res = tuple(res)
        self.assertEqual(res[3], "updatedexe", 
                "Seems not to be updated correctly")

    def test_conform(self):
        """ Test for sqlite3 representation
        """
        self.comp.create_table()
        repr = self.comp.__conform__(sqlite3.PrepareProtocol)
        self.assertEqual(repr, "c_id=name;c_exe=/path/to/exe;c_ci=/path/to/ci",
                msg="Error in generation of representation")

    def test_convert(self):
        """ Tests if a __conform__ representation could be successfully
        rebuild.
        """
        self.comp.create_table()
        repr =  "c_id=name;c_exe=/path/to/exe;c_ci=/path/to/ci"
        comp = Component.convert(repr)
        self.assertEqual(comp, self.comp)

    def test_get(self):
        from datetime import datetime
        from datetime import timedelta
        self.comp.create_table()
        self.comp.save()
        # Test get all
        comps = Component.get()
        self.assertEqual(comps[0], self.comp, "Could not deserialize data")
        time_since = datetime.today() - timedelta(minutes=10)
        comps = Component.get(time_since)
        Log.debug("test_get(): comps: "+ str(comps))
        self.assertEqual(comps[0], self.comp, "Could not deserialize data")

    def test_get_exacly(self):
        self.comp.create_table()
        self.comp.save()
        comp = Component.get_exacly(self.comp.c_id)
        self.assertEqual(comp, self.comp, "Could not deserialize data")

if __name__ == '__main__':
    unittest.main()
