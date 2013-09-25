#!/usr/bin/env python3
import unittest

import os
import sys

lib_path = os.getcwd() + "/../../lib/backend"
sys.path.append(lib_path)
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
                        Database = test.db
                        Manifest_store = /dev/null
                        authorized_keys = auth_keys""")
        return conffile

    def setUp(self):
        Database.db_file = None  # else the runtime destroys testsing framework
        Database(self.gentest_config())
        self.user = User("Douglas")
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
        self.assertFalse(result is None,
                         "Table user could not been found")
        for i in result:
            if 'User' in i:
                table_exists = True
        self.assertTrue(table_exists)

    def test_drop_table(self):
        self.user.create_table()
        self.user.drop_table()
        self.cursor.execute("""SELECT name FROM sqlite_master
                            WHERE name = 'User';""")
        self.assertTrue(self.cursor.fetchone() is None,
                        "Database could not been droped")

    def test_getitem(self):
        self.user.create_table()
        self.assertEqual(self.user["c_id"], "Douglas")
#        self.assertEqual(self.user["c_pubkey"], "pubkey")
        try:
            self.user["db_file"]
            self.assertTrue(False, "Was able to caught wrong attribute")
        except AttributeError:
            pass

    def test_get_attributes(self):
        self.user.create_table()
        attrs = self.user.get_attributes()
        self.assertTrue("c_id" in attrs)
#        self.assertTrue("c_pubkey" in attrs)
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
#       First, try to get data
        self.cursor.execute("""SELECT * FROM User""")
        result = self.cursor.fetchall()
        self.assertEqual(len(result), 1, "too much or too less objects")
        self.cursor.execute("""SELECT * FROM User
                WHERE c_id = 'Douglas';""")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result,
                             "Couldn't read data from database")
        result = tuple(result)
        self.assertEqual(result[3], 'Douglas')

    def test_remove(self):
        self.user.create_table()
        self.user.save()
        for key in self.user.get_keys():
            key.save()
        self.user.remove()
        self.cursor.execute("""SELECT * FROM User
                            WHERE c_id = 'Douglas';""")
        self.assertTrue(self.cursor.fetchone() is None,
                        "Removing Entries has failed")

    def test_get(self):
        self.user.create_table()
        self.user.save()
        results = User.get()
        self.assertEqual(self.user, results[0], "Unable to get all data")
        import datetime
        d = datetime.datetime.now() - datetime.timedelta(minutes=2)
        results = User.get(d)
        self.assertEqual(self.user, results[0], "Unable to get new data")

    def test_get_exactly(self):
        self.user.create_table()
        self.user.save()
        user = User.get_exactly(self.user.c_id)
        self.assertEqual(user, self.user, "Could not deserialize data")

    def test_override(self):
        """ This function tests the default override procedure. """
        self.user.create_table()
        self.user.save()
        user2 = User('Douglas')
        user2.save()

    def test_pubkeys(self):
        from collections import Counter
        self.user.create_table()
        self.user.save()
        self.user.add_key("pubkey")
        self.user.add_key('second_pubkey')
        self.user.add_key('third_pubkey')
        self.assertEqual(Counter(['pubkey', 'second_pubkey', 'third_pubkey']),
                         Counter([i.c_key for i in self.user.get_keys()]),
                         'did not save keys')
        user = User.get_exactly(self.user.c_id)
        self.assertEqual(Counter(['pubkey', 'second_pubkey', 'third_pubkey']),
                         Counter([i.c_key for i in user.get_keys()]),
                         'did not load keys')


class TestAddUser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_key(self):
        pass

    def test_remove_key(self):
        pass

    def test_add(self):
        pass

    def test_remove(self):
        pass


if __name__ == "__main__":
    unittest.main()
