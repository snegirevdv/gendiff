import json
from typing import Any

from gendiff.constants import CHANGED, DELETED
from gendiff.format.constants import AFTER, BEFORE, STATUS, VALUE


def json_format(
    diff: dict[str, str | dict[str, Any]],
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> str:
    """
    Format the diff in a standard JSON style.

    Args:
        diff: diff dictionary.
        dict1, dict2: compared dictionaries.

    Returns:
        Formatted diff view.
    """
    merged_data = merge_dicts(diff, dict1, dict2)
    return json.dumps(merged_data, indent=3)


def merge_dicts(
    diff: dict[str, str],
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    merged_data = {}

    for key, status in sorted(diff.items()):
        value1, value2 = dict1.get(key), dict2.get(key)
        merged_data[key] = get_merged_value(status, value1, value2)

    return merged_data


def get_merged_value(
    status: dict[str, Any] | str,
    value1: Any,
    value2: Any,
) -> dict[str, Any]:
    if isinstance(status, dict):
        return merge_dicts(diff=status, dict1=value1, dict2=value2)

    if status == CHANGED:
        return {STATUS: CHANGED, BEFORE: value1, AFTER: value2}

    if status == DELETED:
        return {STATUS: status, VALUE: value1}

    return {STATUS: status, VALUE: value2}
