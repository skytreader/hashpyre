#! usr/bin/env python

from hashpyre import FileParser

import unittest

class FileParserTest(unittest.TestCase):
    
    def setUp(self):
        self.valid_keys = ("simplekey", "with_underscore",
            "314159265358979", "numb3rm1x", "und3rsc0r3d_31415")
        self.invalid_keys = ("with spacing", "spaced 123")


    def test_key_regex(self):
        for valid in self.valid_keys:
            self.assertTrue(FileParser.KEY_REGEX.match(valid))

        for invalid in self.invalid_keys:
            self.assertFalse(FileParser.KEY_REGEX.match(invalid))

if __name__ == "__main__":
    unittest.main()
