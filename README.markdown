# Hashpyre...

A simple "language" to insert hashmaps to Redis.

# Usage

Invoke the script with the following arguments:

- **-f** _required_  
Indicates the filename of the hashmap inserts.

- **-h** _required_  
The Redis server host IP.

- **-p** _required_  
The Redis server host port.

- **-s**  
The Redis server password, when applicable.

**Sample Invocation**

    python hashpyre.py -finserts.txt -hlocalhost -p6379

To invoke `hashpyre` on a file named `inserts.txt` to be inserted on the local Redis server at port 4096.

# Insert File Structure

There are four kinds of lines/statements in an insert file:

- **Map name declaration**  
A map name is a single word consist of alphanumeric or underscore characters in a line all by itself. This
is used as the name of the map once inserted to Redis.

- **map()**  
Inserts all the assignment lines _after the last invocation of map()_ as a single hash map in Redis. This
throws an error if a new map name has not been declared since the last map() invocation.

- **Assignment lines**  
Most probably going to be the most common line in an insert file. Sets a key-value pairing for the current hashmap.
Assignment lines are of the form:

    [KEY] :[VALUE]

Where key is a single word consist of alphanumeric or underscore characters and value is a string made up of alphanumeric
and punctuation characters with possible spaces. Note that there may be any number of spaces between the key and colon but
everything after the colon is considered part of the value.

- **Comments**  
Comments are lines that start with the hash character (`#`). These lines (along with blank lines) are ignored by
Hashpyre.

**Sample Insert File**

    # This is a comment. It will be ignored by Hashpyre.
    
    # The following line is a hash name. Though not required,
    # it is a good idea to declare the hash name right after the
    # last map() invocation (or, in this case, the start of the file).
    BOOKS_1
    # Mappings follow...
    title :Aesthetic Computing
    Publisher :MIT Press
    editor:Paul A. Fishwick
	ISBN  :9780262562379
    # Send map BOOKS_1 to Redis
    map()
