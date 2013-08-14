#!/usr/bin/env python3
import unittest

class TestBasicInit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_call(self):
        from subprocess import call
        exit_code = call(['ctl-init'])
        self.assertEqual(exit_code, 1)

        # check if the ctl-call is working
        exit_code = call(['ctl_init'])
        self.assertEqual(exit_code, 1)

if __name__ == '__main__':
    unittest.main()
