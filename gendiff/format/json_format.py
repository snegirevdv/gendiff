import json
from typing import Any

from gendiff.constants import NESTED, STATUS, VALUE


def json_format(diff: dict[str, dict[str, Any]]) -> str:
    """
    Format the diff in a standard JSON style.

    Args:
        diff: diff dictionary.
        dict1, dict2: compared dictionaries.

    Returns:
        Formatted diff view.
    """
    pure_diff = get_pure_diff(diff)
    return json.dumps(pure_diff, indent=3)


def get_pure_diff(diff: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    new_diff = {}
    for key, item in diff.items():
        if item[STATUS] == NESTED:
            new_diff[key] = get_pure_diff(item[VALUE])
        else:
            new_diff[key] = diff[key]

    return new_diff
