from typing import Any, Callable

from gendiff import constants as const
from gendiff import parser
from gendiff.format import json_format, plain, stylish

FORMATTERS = {
    const.STYLISH: stylish.get_view,
    const.PLAIN: plain.get_view,
    const.JSON: json_format.get_view,
}


def generate_diff(
    file1_path: str,
    file2_path: str,
    format: str = const.STYLISH
) -> str:
    """
    Generate a textual formatted diff report between two files.

    Args:
        file1_path: Path to the first file to compare.
        file2_path: Path to the second file to compare.
        formatter (optional): Function to format the diff output.

    Formatter Options:
        stylish (default): JSON-like format, changes marked by "+" and "-".
        plain: textual report of changes, shows property updates.
        json_format: standard JSON format representation.
    """
    parsed_data = parser.parse_data_from_files(file1_path, file2_path)
    diff = create_diff(*parsed_data)
    formatter = get_formatter(format)

    return formatter(diff)


def create_diff(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, dict[str, Any] | list[Any]]:
    """
    Create a dictionary representing the diff between two dictinaries.

    Returns:
        Dictionary contains keys from both dicts.
        Key's values contain lists describing the changes.
        For nested dictionaries values contain recursive diff dictionaries.
    """
    keys = set(dict1).union(dict2)
    return {key: create_item(key, dict1, dict2) for key in keys}


def create_item(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, Any] | list[Any]:
    if is_nested_diff(key, dict1, dict2):
        return create_diff(dict1=dict1[key], dict2=dict2[key])

    status = calculate_status(key, dict1, dict2)

    if status == const.CHANGED:
        return [status, dict1[key], dict2[key]]

    diff_value = dict1.get(key) if key in dict1 else dict2[key]

    return [status, diff_value]


def calculate_status(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any]
) -> str:
    value1, value2 = dict1.get(key), dict2.get(key)

    if key not in dict1:
        return const.ADDED

    if key not in dict2:
        return const.DELETED

    if value1 == value2:
        return const.UNCHANGED

    return const.CHANGED


def is_nested_diff(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any]
) -> bool:
    value1, value2 = dict1.get(key), dict2.get(key)
    return (
        isinstance(value1, dict)
        and isinstance(value2, dict)
        and value1 != value2
    )


def get_formatter(format: str) -> Callable:
    return FORMATTERS[format]
