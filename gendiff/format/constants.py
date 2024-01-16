from gendiff.constants import ADDED, CHANGED, DELETED, UNCHANGED

VALUE_CONVERTOR = {
    True: "true",
    False: "false",
    None: "null",
}

# Stylish
INDENT_SIZE = 4
INDENT_SYMBOL = " "

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
