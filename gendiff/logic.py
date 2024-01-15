from collections.abc import Callable

from gendiff import format, parser
from gendiff.constants import ADDED, CHANGED, DELETED, UNCHANGED


def generate_diff(file1: str, file2: str,
                  formatter: Callable = format.stylish) -> str:
    data = parser.parse_data(file1, file2)
    diff = get_diff(*data)
    return formatter(diff, *data)


def get_diff(dict1: dict, dict2: dict) -> dict:
    keys_1 = set(dict1)
    keys_2 = set(dict2)

    changed = dict.fromkeys(
        set(filter(lambda key: dict1[key] != dict2[key], keys_1 & keys_2)),
        CHANGED)
    unchanged = dict.fromkeys(keys_1 & keys_2 - set(changed), UNCHANGED)
    deleted = dict.fromkeys(keys_1 - keys_2, DELETED)
    added = dict.fromkeys(keys_2 - keys_1, ADDED)

    for key in changed:
        value1, value2 = dict1[key], dict2[key]
        if isinstance(value1, dict) and isinstance(value2, dict):
            changed[key] = get_diff(value1, value2)

    return unchanged | changed | deleted | added
