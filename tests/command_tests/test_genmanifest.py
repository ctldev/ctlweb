#!/usr/bin/env python3
import unittest

class TestBasicGenmanifest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_call(self):
        from subprocess import call
        exit_code = call(['ctl-genmanifest'])
        self.assertEqual(exit_code, 1)


if __name__ == '__main__':
    unittest.main()
