# Formats
STYLISH = "stylish"
PLAIN = "plain"
JSON = "json"

# Diff statuses
DELETED = "deleted"
UNCHANGED = "unchanged"
ADDED = "added"
CHANGED = "changed"

# Stylish settings
INDENT_SIZE = 4
INDENT_SYMBOL = " "

PREFIXES = {
    DELETED: "-",
    UNCHANGED: " ",
    ADDED: "+",
}

# Parser settings
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
