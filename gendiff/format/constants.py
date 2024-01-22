from gendiff import constants as const

# Common
VALUE_CONVERTOR = {
    True: "true",
    False: "false",
    None: "null",
}

# Stylish
INDENT_SIZE = 4

SPACE = " "
START_LINE = "{\n"
FINISH_LINE = "}\n"

PREFIXES = {
    const.DELETED: "-",
    const.UNCHANGED: " ",
    const.ADDED: "+",
}

# Plain
PROPERTY = "Property"
COMPLEX = "[complex value]"
DELIMETER = "."

MESSAGES = {
    const.ADDED: "was added with value: {values[0]}",
    const.DELETED: "was removed",
    const.CHANGED: "was updated. From {values[0]} to {values[1]}",
}
