#! usr/bin/env python

import re
import redis

"""
Creates hashmap values in redis based on a text file. Can also
put the hashmap names on a list.

@author Chad Estioco
"""

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
		self.hash_table = {}

class FileParser(object):
	"""
	Parses our text file and interacts with redis based on it.
	The format of the text file is as follows:

		- Assignment lines of the form

		    <key>\s*<separator>\s*<value>

		  Where separator is a one-character delimiter, key is an
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
	KEY = r"\w+"
	KEY_REGEX = re.compile(KEY)
	DEFAULT_SEPARATOR = ":"
	VALUE = r"[\w\s]+"
	VALUE_REGEX = re.compile(VALUE)
	ASSIGNMENT = KEY + r"\s*" + DEFAULT_SEPARATOR + r"\s*" + VALUE
	ASSIGNMENT_REGEX = re.compile(ASSIGNMENT)

	HASH_NAME = r"\w+"
	HASH_NAME_REGEX = re.compile(HASH_NAME)
	
	# TODO Might have to add more parameters here for security
	def __init__(self, host, port, password):
		# TODO Check what happens when redis server does not respond as expected
		self.__redis = redis.StrictRedis(host=host, port=port, password=password)

	@property
	def separator(self):
		return self.__separator
	
	@separator.setter
	def separator(self, s):
		if not len(s):
			raise SettingException("Separators should be one character only.")
		self.__separator = s
	
	# TODO Indicate what line number did the error occur
	def parse(filename):
		redis_hash = RedisHash()

		with open(filename, "r") as map_file:
			for line in map_file:
				if ASSIGNMENT_REGEX.match(line):
					# Parse the line
					line_parse = line.split(r"\s*" + DEFAULT_SEPARATOR + r"\s*")
					redis_hash.hash_map[line_parse[0]] = line_parse[1]
				elif HASH_NAME_REGEX.match(line):
					redis_hash.hash_name = line
				elif line == "map()":
					if redis_hash.hash_name is None:
						raise InvalidCommandSequenceException("Hash name is not set since the last invocation of map()")
					self.__redis.hmset(redis_hash.hash_name, redis_hash.hash_map)
					print "Inserted map " + redis_hash.hash_name
				elif line[0] != "#":
					raise UnknownCommandException("This line does not match the grammar: " + line)
