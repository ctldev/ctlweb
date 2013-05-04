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
        Log.streamoutput()
#       Instance objects
        self.comp = Component("name","/path/to/exe")
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
        self.assertEqual(res[3], "name", "Got unexpected data")
        self.assertEqual(res[2], "/path/to/exe", "Got unexpected data")
        #updatecheck
        self.comp.c_exe = "updatedexe"
        self.comp.save()
        cursor.execute("SELECT * FROM Component;")
        res = cursor.fetchone()
        res = tuple(res)
        self.assertEqual(res[2], "updatedexe", 
                "Seems not to be updated correctly")

    def test_remove(self):
        self.comp.create_table()
        self.comp.save()
        try:
            self.comp.remove()
        except OSError:
            pass # The error that is risen because of the missing component
                 # file. This test will be repeated in class TestComponentAdd
        self.cursor.execute("""SELECT * FROM Component
                            WHERE c_id = 'name';""")
        self.assertTrue(self.cursor.fetchone() == None, 
                "Removing Entries has failed")

    def test_conform(self):
        """ Test for sqlite3 representation
        """
        self.comp.create_table()
        repr = self.comp.__conform__(sqlite3.PrepareProtocol)
        self.assertEqual(repr,
                "c_id=name;c_exe=/path/to/exe",
                msg="Error in generation of representation")

    def test_convert(self):
        """ Tests if a __conform__ representation could be successfully
        rebuild.
        """
        self.comp.create_table()
        repr =  "c_id=name;c_exe=/path/to/exe"
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

class TestComponentAdd(unittest.TestCase):
    """ Full tests for adding compontents
    """

    def setUp(self):
        import os
        self.component = None # tgz file
        self.test_folder = None # folder where you'll find the evil
        self.control = None # contol-file
        self.ci = None # ci file
        self.doc = None # component documentation
        self._create_component()
        Database.db_file = os.path.join(self.test_folder, 'test.db')
        Database.store = os.path.join(self.test_folder, 'store')
        os.mkdir(Database.store)

    def tearDown(self):
        import os
        for f in os.listdir( os.path.join(self.test_folder, 'store')):
            os.remove( os.path.join(self.test_folder, 'store', f))
        os.rmdir( os.path.join(self.test_folder, 'store'))
        for f in os.listdir(self.test_folder):
            os.remove(os.path.join(self.test_folder, f))
        os.rmdir(self.test_folder)

    def test_read_control(self):
        """ checks if the control parsing is done correctly
        """
        data = Component._read_control(self.control)
        self.assertEqual(data, {"c_id": "example",
                "c_exe": "/home/foo/example.exe",
                },
                )

    def test_unpack(self):
        """ checks if unpacking is done correctly
        """
        data = Component._unpack(self.component)
        self.assertEqual(data, {"c_id": "example",
                "c_exe": "/home/foo/example.exe",
                },
                )

    def test_add(self):
        """ depends kind of the previous tests, checks only if the database
        entry it really done and the file is moved to the storage
        """
        insert = Component.add(self.component)
        output = Component.get_exacly("example")
        self.assertEqual(insert, output)
        # check if component is stored.
        import os
        self.assertTrue( os.path.isfile(
                os.path.join(Database.store, 'example.tgz')
            ))

    def test_remove(self):
        """ This Test is a complete test for the removal function. It tests the
        removal of a database entry as well as the correlated file in the store
        """
        component = Component.add(self.component)
        component.remove()
        cursor = Database.db_connection.cursor()
        cursor.execute("""SELECT * FROM Component
                            WHERE c_id = 'name';""")
        self.assertTrue(cursor.fetchone() == None, 
                "Removing Entries has failed")
        import os
        component_file = os.path.join( Database.store, "example.tgz" )
        self.assertFalse( os.path.isfile( component_file ) )

    def _create_component(self):
        """ creates a full (dummy) ctl-component for testing purpose.
        """
        import os
        self.test_folder = '/tmp/ctlweb_test'
        self.control = os.path.join(self.test_folder, 'control')
        self.ci = os.path.join(self.test_folder, 'test.ci')
        self.doc = os.path.join(self.test_folder, 'doc.txt')
        os.mkdir(self.test_folder)
        with open(self.control, "w") as f:
            f.write("""[DEFAULT]
            name=example
            host=example.net
            user=foo
            ssh=22
            exe=/home/foo/example.exe
            exe_hash=uitaen2f3c2g3fnelren234234234n123rt4r
            ci=test.ci""")
        open(self.ci, "w").close()
        open(self.doc, "w").close()
        self._pack_component()

    def _pack_component(self):
        """ packs files to a component
        """
        import tarfile
        self.component = '/tmp/ctlweb_test/test.tgz'
        with tarfile.open(self.component, 'w:gz') as tf:
            tf.add(self.control, arcname="control")
            tf.add(self.ci, arcname="test.ci")
            tf.add(self.ci, arcname="doc.txt")


if __name__ == '__main__':
    unittest.main()
