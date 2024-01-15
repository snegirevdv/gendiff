import itertools
from collections.abc import Hashable
from typing import Any

from gendiff import parser

DELETED = "deleted"
UNCHANGED = "unchanged"
ADDED = "added"
CHANGED = "changed"

INDENT_STEP = 4

PREFIXES = {
    DELETED: "-",
    UNCHANGED: " ",
    ADDED: "+",
}


def generate_diff(file1: str, file2: str) -> str:
    dict1, dict2 = parser.parse_data(file1, file2)
    diff = get_diff(dict1, dict2)
    return get_diff_report(diff, dict1, dict2).rstrip()


def get_diff(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[tuple[Hashable, int], Any]:
    keys_1 = set(dict1)
    keys_2 = set(dict2)

    changed = dict.fromkeys(
        filter(lambda key: dict1[key] != dict2[key], keys_1 & keys_2),
        CHANGED)
    unchanged = dict.fromkeys(
        filter(lambda key: dict1[key] == dict2[key], keys_1 & keys_2),
        UNCHANGED)
    deleted = dict(zip(keys_1 - keys_2, itertools.repeat(DELETED)))
    added = dict(zip(keys_2 - keys_1, itertools.repeat(ADDED)))

    return unchanged | changed | deleted | added


def get_diff_report(diff: dict, dict1, dict2, indent=0) -> str:
    result = "{\n"
    for key, difference in sorted(diff.items()):
        result += get_lines(key, difference, dict1, dict2, indent)
    result += get_indent(indent) + "}\n"
    return result


def get_line_view(prefix: str, key: Hashable, value, indent) -> str:
    return f"{get_indent(indent)}  {prefix} {key}: {value}\n"


def get_dict_view(dictionary, indent):
    result = "{\n"
    for sub_key in dictionary:
        prefix = PREFIXES[UNCHANGED]
        value = dictionary[sub_key]
        result += get_line_or_dict(prefix, sub_key, value, indent + 1)
    result += get_indent(indent + 1) + "}\n"
    return result


def get_line_or_dict(prefix, key, value, indent):
    if isinstance(value, dict):
        return f"{get_indent(indent)}  {prefix} {key}: " + get_dict_view(value, indent)
    return get_line_view(prefix, key, value, indent)


def get_lines(key, difference, dict1: dict, dict2: dict, indent):
    value1 = dict1.get(key)
    value2 = dict2.get(key)
    prefix = PREFIXES.get(difference)

    if difference in (DELETED, UNCHANGED):
        return get_line_or_dict(prefix, key, value1, indent)
    if difference == ADDED:
        return get_line_or_dict(prefix, key, value2, indent)
    if isinstance(value1, dict) and isinstance(value2, dict):
        new_diff = get_diff(value1, value2)
        return f"{get_indent(indent)}    {key}: " + get_diff_report(new_diff, value1, value2, indent + 1)
    return get_line_or_dict(
        PREFIXES[DELETED], key, value1, indent) + get_line_or_dict(
            PREFIXES[ADDED], key, value2, indent)


def get_indent(indent):
    return " " * INDENT_STEP * indent
