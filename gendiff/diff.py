from typing import Any

from gendiff import consts


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
    return [create_diff_item(key, dict1, dict2) for key in keys]


def create_diff_item(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, Any]:
    status = calculate_status(key, dict1, dict2)

    if is_nested_diff(key, dict1, dict2) and status == consts.CHANGED:
        return {
            consts.KEY: key,
            consts.STATUS: consts.NESTED,
            consts.ELEMENTS: get_diffs(dict1.get(key), dict2.get(key)),
        }

    if status == consts.CHANGED:
        return {
            consts.KEY: key,
            consts.STATUS: status,
            consts.BEFORE: dict1[key],
            consts.AFTER: dict2[key],
        }

    value = dict1.get(key) if key in dict1 else dict2.get(key)

    return {
        consts.KEY: key,
        consts.STATUS: status,
        consts.VALUE: value,
    }


def calculate_status(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any]
) -> str:
    value1, value2 = dict1.get(key), dict2.get(key)

    if key not in dict1:
        return consts.ADDED

    if key not in dict2:
        return consts.DELETED

    if value1 == value2:
        return consts.UNCHANGED

    return consts.CHANGED


def is_nested_diff(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any]
) -> bool:
    return (
        isinstance(dict1.get(key), dict)
        and isinstance(dict2.get(key), dict)
    )


def get_status(diff_item: dict[str, Any]) -> str:
    return diff_item[consts.STATUS]


def get_key(diff_item: dict[str, Any]) -> str:
    return diff_item[consts.KEY]


def get_nested_elements(diff_item: dict[str, Any]) -> dict[str, Any]:
    return diff_item[consts.ELEMENTS]


def get_changed_values(diff_item: dict[str, Any]) -> tuple[Any, Any]:
    return diff_item[consts.BEFORE], diff_item[consts.AFTER]


def get_value(diff_item: dict[str, Any]) -> Any:
    return diff_item[consts.VALUE]
