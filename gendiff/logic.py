from collections.abc import Hashable
from typing import Any

from gendiff import parser

LINE_PREFIX_VALUES = {
    -1: "-",
    0: " ",
    1: "+",
}


def generate_diff(file1: str, file2: str) -> str:
    dict1, dict2 = parser.parse_data(file1, file2)
    merged_data = merge_dicts(dict1, dict2)
    return get_diff_report(merged_data)


def merge_dicts(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[tuple[Hashable, int], Any]:
    merged = {}
    keys_1 = set(dict1)
    keys_2 = set(dict2)

    unchanged_keys = set(
        filter(lambda key: dict1[key] == dict2[key], keys_1 & keys_2)
    )
    changed_keys = set(
        filter(lambda key: dict1[key] != dict2[key], keys_1 & keys_2)
    )
    deleted_keys = keys_1 - keys_2
    added_keys = keys_2 - keys_1

    for key in unchanged_keys:
        merged[(key, 0)] = dict1[key]

    for key in deleted_keys | changed_keys:
        merged[(key, -1)] = dict1[key]

    for key in added_keys | changed_keys:
        merged[(key, 1)] = dict2[key]

    return merged


def get_diff_report(data: dict) -> str:
    result = "{\n"
    for key_tuple, value in sorted(data.items()):
        key, prefix_key = key_tuple
        line = f"  {LINE_PREFIX_VALUES[prefix_key]} {key}: {value}\n"
        result += line
    result += "}"
    return result
