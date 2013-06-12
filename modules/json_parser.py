#!/usr/bin/python

import simplejson as json

class JsonSchemaParser:
    @staticmethod
    def read(msgs):
        res = []
        for msg in msgs:
            res.append(json.loads(msg))
        return res
