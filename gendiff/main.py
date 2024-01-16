from collections.abc import Callable
from typing import Any

from gendiff import parser, stylish
from gendiff.constants import ADDED, CHANGED, DELETED, UNCHANGED


def generate_diff(file1: str, file2: str,
                  formatter: Callable = stylish) -> str:
    """
    Generate a diff between two files.

    Args:
        file1: Path to the first file to compare.
        file2: Path to the second file to compare.
        formatter (optional): Function to format the diff output.

    Formatter Options:
        stylish (default): JSON-like format, changes marked by "+" and "-".
        plain: textual report of changes, shows property updates.
        json_format: standard JSON format representation.

    Returns:
        Formatted diff string representing the differences.

    """
    data = parser.parse_data_from_files(file1, file2)
    diff = get_diff(*data)
    return formatter(diff, *data)


def get_diff(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """
    Generates a diff between two dictionaries.

    The returned dictionary structure:
        Keys: Union of keys from both dictionaries.
        Values: Status of the diff for each key.
                Options: unchanged, changed, deleted, added.
                For nested dictionaries, the values are diff dictionaries.
    """
    def have_equal_values(key):
        return dict1[key] == dict2[key]

    keys_1 = set(dict1)
    keys_2 = set(dict2)
    common_keys = keys_1.intersection(keys_2)

    unchanged = dict.fromkeys(filter(have_equal_values, common_keys), UNCHANGED)
    changed = dict.fromkeys(common_keys.difference(unchanged), CHANGED)
    deleted = dict.fromkeys(keys_1.difference(keys_2), DELETED)
    added = dict.fromkeys(keys_2.difference(keys_1), ADDED)

    for key in changed:
        value1, value2 = dict1[key], dict2[key]
        if isinstance(value1, dict) and isinstance(value2, dict):
            changed[key] = get_diff(value1, value2)

    diff = dict(**unchanged, **changed, **deleted, **added)

    return dict(sorted(diff.items()))
