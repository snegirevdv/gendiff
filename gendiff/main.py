from typing import Any, Callable

from gendiff import constants as const
from gendiff import parser
from gendiff.format import json_format, plain, stylish

FORMATTERS = {
    const.STYLISH: stylish.get_view,
    const.PLAIN: plain.get_view,
    const.JSON: json_format.get_view,
}


def generate_diff(file1: str, file2: str, format: str = "stylish") -> str:
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
    formatter = get_formatter(format)

    return formatter(diff)


def create_diff(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, dict[str:Any] | list[Any]]:
    """
    Create a diff dictionary representing the diff between two dictinaries.

    Returns:
        Dictionary contains keys from both dicts.
        Key's values contain lists dictionary describing the changes.
        For nested dictionaries values contain recursive diff dictionaries.
    """
    keys = set(dict1).union(dict2)
    return {key: create_item(key, dict1, dict2) for key in keys}


def create_item(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, Any] | list[Any]:
    if is_nested(key, dict1, dict2):
        return create_diff(dict1=dict1[key], dict2=dict2[key])

    status = get_status(key, dict1, dict2)

    if status == const.CHANGED:
        return [status, dict1[key], dict2[key]]

    value = dict1.get(key) if key in dict1 else dict2[key]

    return [status, value]


def get_status(key: str, dict1: dict[str, Any], dict2: dict[str, Any]) -> str:
    v1, v2 = dict1.get(key), dict2.get(key)

    if key not in dict1:
        return const.ADDED

    if key not in dict2:
        return const.DELETED

    if v1 == v2:
        return const.UNCHANGED

    return const.CHANGED


def is_nested(key: str, dict1: dict[str:Any], dict2: dict[str:Any]) -> bool:
    v1, v2 = dict1.get(key), dict2.get(key)
    return isinstance(v1, dict) and isinstance(v2, dict) and v1 != v2


def get_formatter(format: str) -> Callable:
    return FORMATTERS[format]
