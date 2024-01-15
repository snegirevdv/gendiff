from gendiff.constants import (
    ADDED,
    CHANGED,
    DELETED,
    INDENT_SIZE,
    INDENT_SYMBOL,
    PREFIXES,
    UNCHANGED,
)


# Stylish
def stylish(diff: dict[str, str], dict1: dict, dict2: dict, step=0):
    report = "{\n"

    for key, value in sorted(diff.items()):
        if isinstance(value, dict):
            report += get_left(step, key)
            report += stylish(value, dict1[key], dict2[key], step + 1)

        elif value == UNCHANGED:
            report += get_left(step, key)
            report += get_right(key, dict2, step + 1)

        else:
            if value in (DELETED, CHANGED):
                report += get_left(step, key, DELETED)
                report += get_right(key, dict1, step + 1)
            if value in (ADDED, CHANGED):
                report += get_left(step, key, ADDED)
                report += get_right(key, dict2, step + 1)

    report += get_indent(step) + "}" + "\n" * bool(step)
    return report


def get_left(step, key, status=UNCHANGED, subdict=False):
    if subdict:
        return f"{get_indent(step + 1)}{key}: "
    return f"{get_indent(step)}  {PREFIXES[status]} {key}: "


def get_right(key, dictionary: dict, step):
    if isinstance(dictionary[key], dict):
        result = "{\n"
        for sub_key in dictionary[key]:
            result += get_left(step, sub_key, subdict=False)
            result += get_right(sub_key, dictionary[key], step + 1)
        result += get_indent(step) + "}\n"
        return result
    return dictionary[key] + "\n"


def get_indent(step):
    return f"{INDENT_SYMBOL * step * INDENT_SIZE}"
