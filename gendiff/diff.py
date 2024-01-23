from typing import Any

from gendiff import consts


def get_diffs(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Creates a list of dictionaries representing the differences
    between two initial dictionaries.

    Returns:
        List contains dictionaries of diff items.
        For nested dictionaries, it contains recursive diff lists.
    """
    keys = sorted(set(dict1).union(dict2))
    return [create_diff_item(key, dict1, dict2) for key in keys]


def create_diff_item(
    key: str,
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, Any]:
    """
    Generates a dictionary representing of a single diff item.

    Returns:
        Dictionary contains the status of the item, key and values.
    """
    status = calculate_status(key, dict1, dict2)

    if status == consts.NESTED:
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

    # The only one dict contains the key or both dicts contain the same value
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
    """
    Determines the status of an item based on its presence and values.

    Options:
        added, deleted, unchanged, nested, or changed.
    """
    value1, value2 = dict1.get(key), dict2.get(key)

    if key not in dict1:
        return consts.ADDED

    if key not in dict2:
        return consts.DELETED

    if value1 == value2:
        return consts.UNCHANGED

    if is_nested_diff(key, dict1, dict2):
        return consts.NESTED

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
