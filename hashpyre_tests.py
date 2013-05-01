#! usr/bin/env python

from hashpyre import FileParser

import unittest

class FileParserTest(unittest.TestCase):
    
    def test_key_regex(self):
        self.assertTrue(FileParser.KEY_REGEX.match("simplekey"))
        self.assertTrue(FileParser.KEY_REGEX.match("with_underscore"))
        self.assertFalse(FileParser.KEY_REGEX.match("with spacing"))
        #pure numbers
        self.assertTrue(FileParser.KEY_REGEX.match("314159265358979"))
        self.assertTrue(FileParser.KEY_REGEX.match("numb3rm1x"))
        self.assertTrue(FileParser.KEY_REGEX.match("und3rsc0r3d_31415"))
        self.assertFalse(FileParser.KEY_REGEX.match("spaced 123"))

if __name__ == "__main__":
    unittest.main()
