#! usr/bin/env python

from hashpyre import FileParser

import unittest

class FileParserTest(unittest.TestCase):
    """
    Assume that FileParser's separator is the colon character ':'
    """

    def setUp(self):
        # TODO Verify with actual redis cli what keys are valid
        self.valid_keys = ("simplekey", "with_underscore",
            "314159265358979", "numb3rm1x", "und3rsc0r3d_31415", "name")
        self.invalid_keys = ("with spacing", "spaced 123")
        
        self.values = ("simplevalue", "value with spaces", "123", "s1mpl3", "m1x3d spac3",
            "!@#$^$%^^&", "This is a well constructed sentence.")

    def test_key_regex(self):
        for valid in self.valid_keys:
            self.assertTrue(FileParser.KEY_REGEX.match(valid))

        for invalid in self.invalid_keys:
            self.assertFalse(FileParser.KEY_REGEX.match(invalid))

    def test_assignment_regex(self):
        self.assertTrue(FileParser.ASSIGNMENT_REGEX.match("name:A Rush of Blood to the Head"))

    def test_value_regex(self):
        for valid in self.values:
            self.assertTrue(FileParser.VALUE_REGEX.match(valid))

if __name__ == "__main__":
    unittest.main()
