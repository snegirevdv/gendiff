from gendiff.constants import (
    ADDED,
    CHANGED,
    DELETED,
    INDENT_SIZE,
    INDENT_SYMBOL,
    PREFIXES,
    UNCHANGED,
)


def stylish(diff: dict[str, str], dict1: dict, dict2: dict, step=0):
    report = "{\n"

    for key, value in sorted(diff.items()):
        if isinstance(value, dict):
            report += stylish_get_left(step, key)
            report += stylish(value, dict1[key], dict2[key], step + 1)

        elif value == UNCHANGED:
            report += stylish_get_left(step, key)
            report += stylish_get_right(key, dict2, step + 1)

        else:
            if value in (DELETED, CHANGED):
                report += stylish_get_left(step, key, DELETED)
                report += stylish_get_right(key, dict1, step + 1)
            if value in (ADDED, CHANGED):
                report += stylish_get_left(step, key, ADDED)
                report += stylish_get_right(key, dict2, step + 1)

    report += stylish_get_indent(step) + "}" + "\n" * bool(step)
    return report


def stylish_get_left(step, key, status=UNCHANGED, subdict=False):
    if subdict:
        return f"{stylish_get_indent(step + 1)}{key}: "
    return f"{stylish_get_indent(step)}  {PREFIXES[status]} {key}: "


def stylish_get_right(key, dictionary: dict, step):
    if isinstance(dictionary[key], dict):
        result = "{\n"
        for sub_key in dictionary[key]:
            result += stylish_get_left(step, sub_key, subdict=False)
            result += stylish_get_right(sub_key, dictionary[key], step + 1)
        result += stylish_get_indent(step) + "}\n"
        return result
    return dictionary[key] + "\n"


def stylish_get_indent(step):
    return f"{INDENT_SYMBOL * step * INDENT_SIZE}"
