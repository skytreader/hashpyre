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

        # Construct the valid and invalid assignment statements
        self.valid_assignments = []
        self.invalid_assignments = []
        self.assignment_separators = [":", " : ", " :"]

        for key in self.valid_keys:
            for value in self.values:
                spam = self.generate_assignments(key, value)
                self.valid_assignments.extend(spam)
        
        for key in self.invalid_keys:
            for value in self.values:
                spam = self.generate_assignments(key, value)
                self.invalid_assignments.extend(spam)

    def generate_assignments(self, key, value):
        """
        Helper function to generate all assignment test
        cases (spacing and quoting cases included, although
        _we don't have quoting cases yet!_).
        """
        assignments = []
        
        for separator in self.assignment_separators:
            assignments.append(key + separator + value)

        return assignments

    def test_key_regex(self):
        for valid in self.valid_keys:
            self.assertTrue(FileParser.KEY_REGEX.match(valid))

        for invalid in self.invalid_keys:
            self.assertFalse(FileParser.KEY_REGEX.match(invalid))

    def test_assignment_regex(self):
        for valid in self.valid_assignments:    
            self.assertTrue(FileParser.ASSIGNMENT_REGEX.match(valid))

        for invalid in self.invalid_assignments:
            self.assertFalse(FileParser.ASSIGNMENT_REGEX.match(invalid))

    def test_value_regex(self):
        for valid in self.values:
            self.assertTrue(FileParser.VALUE_REGEX.match(valid))

if __name__ == "__main__":
    unittest.main()
