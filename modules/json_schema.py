import re
from collections import defaultdict
from datetime import datetime, date, time


class SchemaFactory:
    def __init__(self, defaultName, output):
        self.__defName = defaultName
        self.__factObject = []
        self.__properties = { }
        self.__output = output + '/'
        # "tag name" : method associate
        self.__generateMap = {
            "{$NAME}"           : self.generateName,
            "{$NAME_UP}"        : self.generateNameUP,
            "{$OBJECT_INIT}"    : self.generateObjectInit,
            "{$STRING_SETTERS}" : self.stringSetters,
            "{$INT_SETTERS}"    : self.intSetters,
            "{$BOOL_SETTERS}"   : self.boolSetters,
            "{$UINT_SETTERS}"   : self.uintSetters,
            "{$DOUBLE_SETTERS}" : self.doubleSetters,
            "{$ARRAY_SETTERS}"  : self.arraySetters,
            "{$OBJECT_SETTERS}" : self.objectSetters,
            "{$STRING_GETTERS}" : self.stringGetters,
            "{$INT_GETTERS}"    : self.intGetters,
            "{$BOOL_GETTERS}"   : self.boolGetters,
            "{$UINT_GETTERS}"   : self.uintGetters,
            "{$DOUBLE_GETTERS}" : self.doubleGetters,
            "{$ARRAY_GETTERS}"  : self.arrayGetters,
            "{$OBJECT_GETTERS}" : self.objectGetters,
            "{$STRING_MEMBERS}" : self.stringMembers,
            "{$INT_MEMBERS}"    : self.intMembers,
            "{$BOOL_MEMBERS}"   : self.boolMembers,
            "{$UINT_MEMBERS}"   : self.uintMembers,
            "{$DOUBLE_MEMBERS}" : self.doubleMembers,
            "{$ARRAY_MEMBERS}"  : self.arrayMembers,
            "{$OBJECT_MEMBERS}" : self.objectMembers,
            "{$DATE}"           : self.date,
            "{$FILENAME}"       : self.filename,
            "{$INCLUDE}"        : self.includes,
            "{$FACT_OBJECT}"    : self.factoryObject,
            "{$FACT_INCLUDES}"  : self.factoryIncludes,
            "{$UNIQUE_ID}"      : self.uniqueId,
            "{$FACT_MEMBERS_INIT}" : self.factMembersInit,
            "{$FACT_MEMBERS}"   : self.factMembers
            }

    def createAnnexe(self):
        template_filename = "templates/error.tplt"
        self.__filename = 'gen_error.hh'
        res = ""
        with open(template_filename, 'r') as f:
            for line in f:
                for (i, j) in self.__generateMap.iteritems():
                    line = line.replace(i + '\n', j())
                    line = line.replace(i, j())
                res += line

        with open(self.__output + r'genjson/include/' + self.__filename, 'w+') as f:
            f.write(res)

        template_filename = "templates/json_object.tplt"
        self.__filename = 'json_object.hh'
        res = ""
        with open(template_filename, 'r') as f:
            for line in f:
                for (i, j) in self.__generateMap.iteritems():
                    line = line.replace(i + '\n', j())
                    line = line.replace(i, j())
                res += line

        with open(self.__output + r'genjson/include/' + self.__filename, 'w+') as f:
            f.write(res)

    def createParser(self):
        template_filename = "templates/parser.tplt"
        self.__filename = 'gen_parser.hh'
        res = ""
        with open(template_filename, 'r') as f:
            for line in f:
                for (i, j) in self.__generateMap.iteritems():
                    line = line.replace(i + '\n', j())
                    line = line.replace(i, j())
                res += line

        with open(self.__output + r'genjson/include/' + self.__filename, 'w+') as f:
            f.write(res)

    def createFactory(self):
        template_filename = "templates/factory.tplt"
        self.__filename = 'gen_factory.hh'
        res = ""
        with open(template_filename, 'r') as f:
            for line in f:
                for (i, j) in self.__generateMap.iteritems():
                    line = line.replace(i + '\n', j())
                    line = line.replace(i, j())
                res += line

        with open(self.__output + r'genjson/include/' + self.__filename, 'w+') as f:
            f.write(res)


    def createObjectClass(self, name, description, properties):
        print "Creating: " + name
        self.__factObject.append(name)
        self.__name = name
        self.__description = description
        self.__properties[name] = properties
        self.__typeMap = defaultdict(list)

        for (nodeName, node) in properties.iteritems():
            self.__typeMap[node["type"]].append((nodeName, node))

        self.generateObjectClass(nodeName,
                                 'gen_json_' + name.lower() + '.hh',
                                 description,
                                 properties)

        for (nodeName, node) in properties.iteritems():
            if node["type"] == "object":
                self.createObjectClass(nodeName,
                                       "",
                                       node["properties"])

    # GENERATION METHODS
    #####################

    def generateObjectClass(self, name, filename, description, properties):
        template_filename = "templates/object_class.tplt"
        self.__filename = filename
        res = ""
        with open(template_filename, 'r') as f:
            for line in f:
                for (i, j) in self.__generateMap.iteritems():
                    line = line.replace(i + '\n', j())
                    line = line.replace(i, j())
                res += line

        with open(self.__output + r'genjson/include/' + self.__filename, 'w+') as f:
            f.write(res)

    def gendefaultName(self):
        return self.__defName

    def includes(self):
        """ Return used include """
        res = ''
        if "string" in self.__typeMap:
            res += '# include <string>\n'
        res += '# include "json_object.hh"\n'
        if "object" in self.__typeMap:
            objs = self.__typeMap["object"]
            for (name, o) in objs:
                res += '# include "gen_json_' + name.lower() + '.hh"\n'

        return res
    def filename(self):
        """ Return filename """
        return self.__filename

    def date(self):
        """ Return generation data """
        return datetime.now().strftime("%a %b %d %H:%M:%S %Y") + '\n'

    def generateName(self):
        """ Return object name """
        return self.__name

    def generateNameUP(self):
        """ Return object name in uppercase """
        return self.__name.upper()

    def generateObjectInit(self):
        """ init member objects with std::make_shared<T> """
        objs = self.__typeMap["object"]
        res = ""
        for (name, o) in objs:
            res += ",\n\t_" + name + " (std::make_shared<Json" + name + ">())"

        return res + '\n'

    def generateSetters(self, typeName, param, isObj=False):
        """ Generate generic setters """
        if typeName not in self.__typeMap:
            return ""

        objs = self.__typeMap[typeName]
        if not objs:
            return ""
        res = "\n    virtual void set" + typeName.capitalize() + '(' + \
            param + " value, const std::string& name)\n    {\n"
        first = True
        for (name, o) in objs:
            if first:
                res += '      if (name == "' + name + '") _' + name
                if isObj:
                    res += ' = std::dynamic_pointer_cast<Json' + name + '>(value);\n'
                else:
                    res += ' = value;\n'
            else:
                res += '    else if (name == "' + name + '") _' + name
                if isObj:
                    res += ' = std::dynamic_pointer_cast<Json' + name + '>(value);\n'
                else:
                    res += ' = value;\n'
            first = False

        res += '      else\n      {\n	__genjson_error += "Can\'t convert `" + name + "\' into ' + typeName + '";\n	__genjson_exc.setError(__genjson_error);\n	throw __genjson_exc;\n      }\n    }'
        return res

    def objectSetters(self):
        """ Generate Object setters"""
        return self.generateSetters("object", "std::shared_ptr<JsonObject>", True)

    def stringSetters(self):
        """ Generate string setters """
        return self.generateSetters("string", "const std::string&")

    def intSetters(self):
        """ Generate int setters """
        return self.generateSetters("integer", "int")

    def boolSetters(self):
        """ Generate bool setters """
        return self.generateSetters("bool", "bool")

    def uintSetters(self):
        """ Generate Uint setters """
        return self.generateSetters("unsigned", "unsigned int")

    def doubleSetters(self):
        """ Generate Double setters """
        return self.generateSetters("number", "double")

    def arraySetters(self):
        """ Generate array setters """
        return self.generateSetters("array", "const Json::Value&")

    def generateGetters(self, typeName, returnType, isObj = False):
        if typeName not in self.__typeMap:
            return ""

        objs = self.__typeMap[typeName]
        res = ''
        for (name, o) in objs:
            res += '\n    ' + returnType
            if isObj:
                res += '<Json' + name + '>'
            res += ' get' + name.capitalize() + '() const\n    {\n      return _' +\
                name + ';\n    }'
        return res

    def stringGetters(self):
        return self.generateGetters("string", "const std::string&")

    def intGetters(self):
        return self.generateGetters("integer", "int")

    def boolGetters(self):
        return self.generateGetters("bool", "bool")

    def uintGetters(self):
        return self.generateGetters("unsigned", "unsigned int")

    def doubleGetters(self):
        return self.generateGetters("number", "double")

    def arrayGetters(self):
        return self.generateGetters("array", "array")

    def objectGetters(self):
        return self.generateGetters("object", "std::shared_ptr", True)
    def uniqueId(self):
        return self.generateGetters("uniqueId", "std::string")

    def generateMembers(self, typeName, returnType, isObj = False):
        if typeName not in self.__typeMap:
            return ""
        objs = self.__typeMap[typeName]
        res = ''
        for (name, o) in objs:
            res += '\n    ' + returnType
            if isObj:
                res += '<Json' + name + '>'
            res += ' _' + name + ';'
        return res

    def stringMembers(self):
        return self.generateMembers("string", "std::string")
    def intMembers(self):
        return self.generateMembers("integer", "int")
    def boolMembers(self):
        return self.generateMembers("bool", "bool")
    def uintMembers(self):
        return self.generateMembers("unsigned", "unsigned int")
    def doubleMembers(self):
        return self.generateMembers("number", "double")
    def arrayMembers(self):
        return self.generateMembers("array", "array")
    def objectMembers(self):
        return self.generateMembers("object", "std::shared_ptr", True)

    def factoryObject(self):
        res = ""
        first = True
        for name in self.__factObject:
            if not first:
                res += '      '
            res += 'if (isJsonEqual(members, _json' + name + '))\n        return new Json' + name + '();\n'
            first = False
        return res

    def factoryIncludes(self):
        res = ""
        for name in self.__factObject:
            res += '# include "gen_json_' + name.lower() + '.hh"\n'
        return res

    def factMembersInit(self):
        res = ""
        for name in self.__factObject:
            lst = []
            for (nodeName, node) in self.__properties[name].iteritems():
                if "required" in node:
                    if node["required"]:
                        lst.append(nodeName)
            lst.sort()
            res += '_json' + name + ' = { "';
            f = True
            for s in lst:
                if f:
                    res += s + '"'
                    f = False
                else:
                    res += ', "' + s + '"'
            res += ' };\n'
        return res

    def factMembers(self):
        res = ""
        for name in self.__factObject:
            res += 'std::vector<std::string> _json' + name + ';\n'

        return res
