# Hashpyre...

A simple "language" to insert hashmaps to Redis.

# Usage

Invoke the script with the following arguments:

**-f** _required_  
Indicates the filename of the hashmap inserts.

**-h** _required_
The Redis server host IP.

**-p** _required_
The Redis server host port.

**-s**
The Redis server password, when applicable.

**Sample Invocation**

    python hashpyre.py -finserts.txt -hlocalhost -p6379

To invoke `hashpyre` on a file named `inserts.txt` to be inserted on the local Redis server at port 4096.
