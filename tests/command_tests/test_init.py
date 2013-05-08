#!/usr/bin/env python3
import unittest

class TestBasicInit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_call(self):
        from subprocess import call
        exit_code = call(['ctl-init', '-v'])
        self.assertEqual(exit_code, 0)

        # check if the ctl-call is working
        exit_code = call(['ctl_init', '-v'])
        self.assertEqual(exit_code, 0)

if __name__ == '__main__':
    unittest.main()
