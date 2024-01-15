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
    def get_block(items):
        key, value = items
        if isinstance(value, dict):
            left = stylish_get_left(key, step)
            right = stylish(value, dict1[key], dict2[key], step + 1)
            return left + right

        if value == UNCHANGED:
            left = stylish_get_left(key, step)
            right = stylish_get_right(key, dict2, step + 1)
            return left + right

        result = ""

        if value in (DELETED, CHANGED):
            result += stylish_get_left(key, step, status=DELETED)
            result += stylish_get_right(key, dict1, step + 1)

        if value in (ADDED, CHANGED):
            result += stylish_get_left(key, step, status=ADDED)
            result += stylish_get_right(key, dict2, step + 1)

        return result

    report = "{\n" + ''.join(map(get_block, sorted(diff.items())))
    report += stylish_get_indent(step) + "}" + "\n" * bool(step)

    return report


def stylish_get_left(key, step, status=UNCHANGED, subdict=False):
    if subdict:
        return f"{stylish_get_indent(step)}{key}: "
    return f"{stylish_get_indent(step)}  {PREFIXES[status]} {key}: "


def stylish_get_right(key, dictionary: dict, step):
    if isinstance(dictionary[key], dict):
        result = "{\n"
        for sub_key in dictionary[key]:
            result += stylish_get_left(sub_key, step + 1, subdict=True)
            result += stylish_get_right(sub_key, dictionary[key], step + 1)
        result += stylish_get_indent(step) + "}\n"
        return result
    return dictionary[key] + "\n"


def stylish_get_indent(step):
    return f"{INDENT_SYMBOL * step * INDENT_SIZE}"
