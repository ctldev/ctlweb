#!/usr/bin/env python3
import unittest

class TestBasicComponent(unittest.TestCase):
    """ Only tests the basic command functions
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_call_program(self):
        from subprocess import call
        exit_code = call(['ctl-component', '-v'])
        self.assertEqual(exit_code, 0)

if __name__ == '__main__':
    unittest.main()
