#!/usr/bin/env python3
import unittest

class TestBasicRegister(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_call(self):
        from subprocess import call
        exit_code = call(['ctl-register'])
        self.assertEqual(exit_code, 1)

if __name__ == '__main__':
    unittest.main()
