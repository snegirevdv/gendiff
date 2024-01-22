from itertools import repeat
from typing import Any
from gendiff import constants as const


def get_diffs(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Create a list of dicts representing the diff between two dictinaries.

    Returns:
        List contains data from both dicts.
        Entries contain the change statuses, and values from both dictionaries.
        For nested dictionaries values contain recursive diff lists.
    """
    keys = sorted(set(dict1).union(dict2))
    return list(map(create_diff_item, keys, repeat(dict1), repeat(dict2)))


def create_diff_item(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, Any] | list[Any]:
    if is_nested_diff(key, dict1, dict2):
        return {
            const.KEY: key,
            const.STATUS: const.NESTED,
            const.ELEMENTS: get_diffs(dict1[key], dict2[key]),
        }

    status = calculate_status(key, dict1, dict2)

    if status == const.CHANGED:
        return {
            const.KEY: key,
            const.STATUS: status,
            const.BEFORE: dict1[key],
            const.AFTER: dict2[key],
        }

    diff_value = dict1.get(key) if key in dict1 else dict2[key]

    return {
        const.KEY: key,
        const.STATUS: status,
        const.VALUE: diff_value,
    }


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


def get_status(diff_item: dict[str, Any]) -> str:
    return diff_item[const.STATUS]


def get_key(diff_item: dict[str, Any]) -> str:
    return diff_item[const.KEY]


def get_nested_elements(diff_item: dict[str, Any]) -> dict[str, Any]:
    return diff_item[const.ELEMENTS]


def get_changed_values(diff_item: dict[str, Any]) -> tuple[Any, Any]:
    return diff_item[const.BEFORE], diff_item[const.AFTER]


def get_value(diff_item: dict[str, Any]) -> tuple[Any, Any]:
    return diff_item[const.VALUE]
