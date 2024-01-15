DELETED = "deleted"
UNCHANGED = "unchanged"
ADDED = "added"
CHANGED = "changed"

INDENT_SIZE = 4
INDENT_SYMBOL = " "

PREFIXES = {
    DELETED: "-",
    UNCHANGED: " ",
    ADDED: "+",
}

VALUE_CONVERTER = {
    True: "true",
    False: "false",
    None: "null",
}

ERRORS = {
    "extension": "ERROR: Files have incorrect extension",
    "not_found": "ERROR: File Not Found",
    "invalid": "ERROR: Files contain invalid data",
}

FORMATS = {
    "JSON": "json",
    "YAML": ("yaml", "yml"),
}
