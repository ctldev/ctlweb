#!/usr/bin/env python3
import unittest
import os
import sys
import sqlite3

lib_path = os.getcwd() + "/../../lib/backend"
sys.path.append( lib_path )
from database.web import Web
from database.database import Database

class TestWeb(unittest.TestCase):

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
        self.web = Web("url", "pubkey")
        self.web.create_table()
        self.cursor = self.web.db_connection.cursor()

    def tearDown(self):
        """ Closes database connection and removes database from disk
        """
        Database.db_connection.close()
        os.remove(self.gentest_config())
        os.remove(Database.db_file)

    def test_create_table(self):
        self.assertIsNotNone(self.web.db_connection, 
                "Database isn't correctly initialized")
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'Web';""")
        table_exists = False
        for i in self.cursor.fetchone():
            if 'Web' in i: table_exists = True
        self.assertTrue(table_exists)

    def test_drop_table(self):
        try:
            self.web.drop_table()
        except sqlite3.OperationalError:
            self.assertFalse(True, "Error while table drop")
        self.cursor.execute("""SELECT name FROM sqlite_master
                WHERE name = 'Web';""")
        self.assertIsNone(self.cursor.fetchone())

    def test_getitem(self):
        """ Tests if access to instance objects with names like c_ are
        possible. Errors or Fails need to be fixed in class Database.
        """
        self.assertEqual(self.web["c_id"], "url" )
        self.assertEqual(self.web["c_pubkey"], "pubkey" )
        try:
            self.web["db_file"]
            self.assertTrue(false, "Got access to wrong variable")
        except AttributeError:
            pass

    def test_get_attributes(self):
        """ Tests if all instance objects are found by get_attributes(). Errors
        or Fails need to be fixed in class Database.
        """
        attrs = self.web.get_attributes()
        self.assertTrue(attrs, msg="Got no attributes")
        self.assertTrue("c_id" in attrs , 
                msg="Caught the following attributes: %s"%attrs)
        self.assertTrue("c_pubkey" in attrs ,
                msg="Caught the following attributes: %s" % attrs)
        self.assertFalse("__doc__" in attrs,
                msg="Caught __doc__ attribute which is wrong")

    def test_save(self):
        """ Checks if data can be made persistent in the database
        """
        self.web.save()
#       connection restart
        self.web.db_connection.close()
        Database()
#       test if data still present
        cursor = self.web.db_connection.cursor()
        cursor.execute("SELECT * FROM Web;")
        res = cursor.fetchone()
        self.assertIsNotNone(res, "Could not read test data from db.")
        res = tuple(res)
        self.assertEqual(res[0], "url", "Got unexpected data")
        self.assertEqual(res[1], "pubkey", "Got unexpected data")


if __name__ == '__main__':
    unittest.main()
