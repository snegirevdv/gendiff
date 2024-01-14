import itertools
from collections.abc import Hashable
from typing import Any

from gendiff import parser

LINE_PREFIXES = {
    "deleted": "-",
    "unchanged": " ",
    "added": "+",
}


def generate_diff(file1: str, file2: str) -> str:
    dict1, dict2 = parser.parse_data(file1, file2)
    diff = make_diff(dict1, dict2)
    return get_diff_report(diff, dict1, dict2)


def make_diff(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[tuple[Hashable, int], Any]:
    keys_1 = set(dict1)
    keys_2 = set(dict2)

    unchanged = dict(zip(
        filter(lambda key: dict1[key] == dict2[key], keys_1 & keys_2),
        itertools.repeat("unchanged")
    ))
    changed = dict(zip(
        filter(lambda key: dict1[key] != dict2[key], keys_1 & keys_2),
        itertools.repeat("changed")
    ))
    deleted = dict(zip(keys_1 - keys_2, itertools.repeat("deleted")))
    added = dict(zip(keys_2 - keys_1, itertools.repeat("added")))

    return unchanged | changed | deleted | added


def get_diff_report(diff: dict, dict1: dict, dict2: dict) -> str:
    result = "{\n"
    for key, difference in sorted(diff.items()):
        if difference in ("deleted", "changed"):
            result += get_line(LINE_PREFIXES["deleted"], key, dict1)
        if difference in ("added", "changed"):
            result += get_line(LINE_PREFIXES["added"], key, dict2)
        if difference == "unchanged":
            result += get_line(LINE_PREFIXES["unchanged"], key, dict1)
    result += "}"
    return result


def get_line(prefix: str, key: Hashable, source: dict[Hashable, Any]):
    return f"  {prefix} {key}: {source[key]}\n"
