from gendiff.constants import (
    ADDED,
    CHANGED,
    DELETED,
    INDENT_SIZE,
    INDENT_SYMBOL,
    PREFIXES,
    UNCHANGED,
)


def get_view(diff: dict[str, str], dict1: dict, dict2: dict, step=0):
    def get_block(items):
        key, value = items
        if isinstance(value, dict):
            left = get_left(key, step)
            right = get_view(value, dict1[key], dict2[key], step + 1)
            return left + right

        if value == UNCHANGED:
            left = get_left(key, step)
            right = get_right(key, dict2, step + 1)
            return left + right

        result = ""

        if value in (DELETED, CHANGED):
            result += get_left(key, step, status=DELETED)
            result += get_right(key, dict1, step + 1)

        if value in (ADDED, CHANGED):
            result += get_left(key, step, status=ADDED)
            result += get_right(key, dict2, step + 1)

        return result

    report = "{\n" + ''.join(map(get_block, sorted(diff.items())))
    report += get_indent(step) + "}" + "\n" * bool(step)

    return report


def get_left(key, step, status=UNCHANGED, subdict=False):
    if subdict:
        return f"{get_indent(step)}{key}: "
    return f"{get_indent(step)}  {PREFIXES[status]} {key}: "


def get_right(key, dictionary: dict, step):
    if isinstance(dictionary[key], dict):
        result = "{\n"
        for sub_key in dictionary[key]:
            result += get_left(sub_key, step + 1, subdict=True)
            result += get_right(sub_key, dictionary[key], step + 1)
        result += get_indent(step) + "}\n"
        return result
    return dictionary[key] + "\n"


def get_indent(step):
    return f"{INDENT_SYMBOL * step * INDENT_SIZE}"
