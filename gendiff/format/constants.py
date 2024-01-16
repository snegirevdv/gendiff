from gendiff.constants import ADDED, CHANGED, DELETED, UNCHANGED

# Common
VALUE_CONVERTOR = {
    True: "true",
    False: "false",
    None: "null",
}

# Stylish
INDENT_SIZE = 4

INDENT_SYMBOL = " "
START_LINE = "{\n"
FINISH_LINE = "}\n"

PREFIXES = {
    DELETED: "-",
    UNCHANGED: " ",
    ADDED: "+",
}

# Plain
PROPERTY = "Property"
COMPLEX = "[complex value]"
DELIMETER = "."

MESSAGES = {
    ADDED: "was added with value: {after}",
    DELETED: "was removed",
    CHANGED: "was updated. From {before} to {after}",
}

# JSON
STATUS = "status"
BEFORE = "before"
AFTER = "after"
VALUE = "value"
