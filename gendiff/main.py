from collections.abc import Callable, Hashable
from typing import Any

from gendiff import parser, stylish
from gendiff.constants import (
    ADDED,
    AFTER,
    BEFORE,
    CHANGED,
    DELETED,
    NESTED,
    STATUS,
    UNCHANGED,
    VALUE,
)


def generate_diff(file1: str, file2: str,
                  formatter: Callable = stylish) -> str:
    """
    Generate a textual diff report between two files.

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
    diff = create_diff(*data)
    return formatter(diff)


def create_diff(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, dict[str, Any]]:

    diff = {}
    keys = set(dict1).union(dict2)

    for key in keys:
        diff[key] = create_item(key, dict1, dict2)

    diff = get_sorted_dict(diff)

    return diff


def create_item(
    key: dict[str, Any] | str,
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, Any]:
    status = get_status(key, dict1, dict2)

    if status == NESTED:
        return {
            STATUS: NESTED,
            VALUE: create_diff(dict1=dict1[key], dict2=dict2[key]),
        }

    if status == CHANGED:
        return {STATUS: CHANGED, BEFORE: dict1[key], AFTER: dict2[key]}

    if status == ADDED:
        return {STATUS: status, VALUE: dict2[key]}

    return {STATUS: status, VALUE: dict1[key]}


def get_status(key: str, dict1: dict[str, Any], dict2: dict[str, Any]) -> str:
    value1, value2 = dict1.get(key), dict2.get(key)

    conditions = {
        ADDED: key not in dict1,
        DELETED: key not in dict2,
        UNCHANGED: value1 == value2,
        NESTED: isinstance(value1, dict) and isinstance(value2, dict),
    }

    for status, condition in conditions.items():
        if condition:
            return status

    return CHANGED


def get_sorted_dict(dictionary: dict[Hashable, Any]) -> dict[Hashable, Any]:
    return dict(sorted(dictionary.items()))
