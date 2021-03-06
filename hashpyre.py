#! usr/bin/env python

import argparse
import re
import redis
import sys

"""
Creates hashmap values in redis based on a text file. Can also
put the hashmap names on a list.

@author Chad Estioco
"""

# CLI-args
HOST = "-host"
PORT = "-port"
PASSWORD = "-password"

# Exceptions

class SettingException(Exception):
    """
    Used when we encounter unexpected settings for our classes.
    """
    def __init__(self, value):    
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class InvalidCommandSequenceException(Exception):
    """
    Used when map() is called without the name being set.
    """
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class UnknownCommandException(Exception):
    """
    For unknown commands (duh)
    """
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

# Actual classes

class RedisHash(object):
    """
    An object representing a hash map that we insert to redis.
    """
    
    def __init__(self):
        self.__hash_name = None
        self.__hash_table = {}

    @property
    def hash_name(self):
        return self.__hash_name
    
    @hash_name.setter
    def hash_name(self, name):
        self.__hash_name = name
    
    @property
    def hash_table(self):    
        return self.__hash_table
    
    def clear(self):    
        self.hash_name == None
        self.__hash_table = {}

class FileParser(object):
    """
    Parses our text file and interacts with redis based on it.
    The format of the text file is as follows:

        - Assignment lines of the form

            <key>\s*<separator>\s*<value>

          Where separator is a one-character delimiter, key is a
          word string (alphanumeric + underscore). Default separator
          is the colon character.
       
       - The name of the list in the form of the a single word (alphanumeric + underscore)
         in a line by itself. If several names appear before the invocation of
         map(), the most recent one is used.

       - The map command in the form of the word 'map()'. This assumes that the
         name of the list has been set beforehand (else we raise an error). Sends
         all the key-value pairs set _after the last invocation of map()_ to redis.

       - A comment line, which starts with a hash "#". Note that there are no inline
         comments.
    """
    
    #TODO Might have to fix this depending on requirements
    # FIXME Handle trailing spaces for all expressions
    KEY = r"\w+"
    """
    The KEY_REGEX desscribes the allowed patterns for hashmap key names.
    (A.K.A, the one paired with the values.)
    """
    KEY_REGEX = re.compile("^" + KEY + "$")
    DEFAULT_SEPARATOR = ":"
    VALUE = r".*"
    """
    The VALUE_REGEX describes the allowed patterns for the values of
    hashmap keys.
    """
    VALUE_REGEX = re.compile(VALUE)
    ASSIGNMENT =  KEY + r"\s*" + DEFAULT_SEPARATOR + VALUE + "$"
    """
    ASSIGNMENT_REGEX describes the pattern of an assignment statement
    in our language.
    """
    ASSIGNMENT_REGEX = re.compile(ASSIGNMENT)

    HASH_NAME = r"\S+"
    """
    HASH_NAME_REGEX describes the allowed patterns for the name of the
    hash to be sent to Redis.
    """
    HASH_NAME_REGEX = re.compile(r"^\s*" + HASH_NAME + r"\s*$")

    BLANK_LINE = r"^\s*$"
    BLANK_LINE_REGEX = re.compile(BLANK_LINE)
    
    # TODO Might have to add more parameters here for security
    def __init__(self, host, port, password = ""):
        # TODO Check what happens when redis server does not respond as expected
        self.__redis = redis.StrictRedis(host=host, port=port, password=password)
        print "Connected to Redis at " + host + ":" + str(port)
        self.__separator = FileParser.DEFAULT_SEPARATOR
        self.__separator_regex = re.compile("\s*" + self.separator + r"\s*")
    
    @property
    def separator_regex(self):
        return self.__separator_regex

    @property
    def separator(self):
        return self.__separator
    
    @separator.setter
    def separator(self, s):
        if not len(s):
            raise SettingException("Separators should be one character only.")
        self.__separator = s
        self.__separtor_regex = re.compile(r"\s*" + s + r"\s*")
    
    # TODO Indicate what line number did the error occur
    def parse(self, filename):
        redis_hash = RedisHash()

        with open(filename, "r") as map_file:
            line_count = 1

            for line in map_file:
                line = line[0:len(line)-1]
                if FileParser.ASSIGNMENT_REGEX.match(line):
                    # Parse the line
                    line_parse = self.separator_regex.split(line, 1)
                    redis_hash.hash_table[line_parse[0]] = line_parse[1]
                    print "Read assignment: " + str(line_parse)
                elif line == "map()":
                    if redis_hash.hash_name is None:
                        raise InvalidCommandSequenceException("Line " + str(line_count) + ": Hash name is not set since the last invocation of map()")
                    # Still not fool-proof. What if redis server goes
                    # away after the ping? :\
                    if self.__redis.ping():
                        self.__redis.hmset(redis_hash.hash_name, redis_hash.hash_table)
                        print "Inserted map " + redis_hash.hash_name
                    else:
                        # Mind the exception for ping. Will never get here
                        print "Redis server unavailable. Skipping transaction: " + redis_hash.hash_name
                    redis_hash.clear()
                elif FileParser.HASH_NAME_REGEX.match(line):
                    redis_hash.hash_name = line
                elif FileParser.BLANK_LINE_REGEX.match(line):
                    pass
                elif line[0] != "#":
                    raise UnknownCommandException("Line " + str(line_count) + ": Does not match the grammar")

                line_count += 1

def run(arg_dictionary):
    if arg_dictionary is None:
        return

    if "-s" in arg_dictionary.keys():
        parser = FileParser(arg_dictionary["host"], arg_dictionary["port"], arg_dictionary["password"])
    else:
        parser = FileParser(arg_dictionary["host"], int(arg_dictionary["port"]))
    
    parser.parse(arg_dictionary["mapfile"])

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(description = "Command-line args for hashpyre.")
	argparser.add_argument(HOST, help = "the address of the Redis server", required=True)
	argparser.add_argument(PORT, help = "the port of the Redis server", type=int, required=True)
	argparser.add_argument(PASSWORD, help = "the password to the Redis server, if required")
	argparser.add_argument("mapfile", help = "the filename containing the mappings to be inserted")
	args_passed = argparser.parse_args()
	run(vars(args_passed))
