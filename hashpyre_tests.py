#! usr/bin/env python

from hashpyre import FileParser

import unittest

class FileParserTest(unittest.TestCase):
    
    def setUp(self):
        self.valid_keys = ("simplekey", "with_underscore",
            "314159265358979", "numb3rm1x", "und3rsc0r3d_31415", "name")
        self.invalid_keys = ("with spacing", "spaced 123")


    def test_key_regex(self):
        for valid in self.valid_keys:
            self.assertTrue(FileParser.KEY_REGEX.match(valid))

        for invalid in self.invalid_keys:
            self.assertFalse(FileParser.KEY_REGEX.match(invalid))

    def test_assignment_regex(self):
        self.assertTrue(FileParser.ASSIGNMENT_REGEX.match("name:A Rush of Blood to the Head"))

    def test_value_regex(self):
        self.assertTrue(FileParser.VALUE_REGEX.match("A Rush of Blood to the Head"))

if __name__ == "__main__":
    unittest.main()
