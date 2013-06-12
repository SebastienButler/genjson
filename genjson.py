#!/usr/bin/python
import sys
import os
import argparse

from modules.json_parser import *
from modules.json_schema import *


def Usage():
    print ("usage")

def process(msgs, output):
    # create archi
    try:
        os.makedirs(output + '/genjson/include/')
    except:
        pass
    props = JsonSchemaParser.read(x[0] for  x in msgs)
    facto = SchemaFactory((x[1] for x in msgs), output)
    for prop in props:
        facto.createObjectClass(prop["name"], "", prop["properties"])

    facto.createFactory()
    facto.createParser()
    facto.createAnnexe()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        parser = argparse.ArgumentParser(description='Json Parser Generator for C++')
        parser.add_argument('list', metavar='json_file;json_name', nargs='+',
                            help='list of all the schema needed to create the parser, each associated with the `jsonObject\' name wanted.')
        parser.add_argument('-o', '--output', metavar='ouput', help='output location.', required=True)
        args = parser.parse_args()
        msgs = []
        for arg in args.list:
            try:
                a = arg.split(';')
                msgs.append((open(a[0], 'r').read(), a[1]))
            except:
                print ("Wrong syntaxe. See help (-h).")
                sys.exit(1)
        process(msgs, args.output)
    except:
        raise

if __name__ == "__main__":
    sys.exit(main())
