GenJson
=======
A json parser generator for C++ written in Python.

GenJson used json schema (see [format][1]) to generate a full C++11 json parser.

Setup
-----
Script requirement:
* python
* simplejson

Generate parser requirement:
* compiler with C++11 specification
* [JsonCpp][2]

Usage
-----
usage: genjson.py [-h] -o ouput json_file;json_name [json_file;json_name ...]

Json Parser Generator for C++

positional arguments:
  json_file;json_name   list of all the schema needed to create the parser,
                        each associated with the `jsonObject' name wanted.

optional arguments:
  -h, --help            show this help message and exit
  -o ouput, --output ouput
                        output location.

Exemple
-------

There is a few schema examples in the test folder with their json associated.
You can use the main.cc in the same folder to see how to use the generated code.
Ex:
$ python genjson.py -o output/ 'test/schema_test.json;product' 'test/schema_lol.json;Lol'
$ cp test/main.cc output/genjson/
$ cd output/genjson && g++ main.cc -std=c++11 -ljson -o genjson
$ ./genjson ../../test/test.json


Todo
----

 * Implement complete json schema specification
 * Add argument to choose boost instead of C++11
 * Improve error message during parsing

[1]: http://json-schema.org/
[2]: http://jsoncpp.sourceforge.net





