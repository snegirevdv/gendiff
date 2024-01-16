import json
from typing import Any

from gendiff.constants import CHANGED, DELETED


def json_format(
    diff: dict[str, str | dict[str, Any]],
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> str:
    merged = merge_dicts(diff, dict1, dict2)
    return json.dumps(merged, indent=3)


def merge_dicts(
    diff: dict[str, str],
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    merged = {}

    for key, status in sorted(diff.items()):
        value1, value2 = dict1.get(key), dict2.get(key)
        merged[key] = get_merged_value(status, value1, value2)

    return merged


def get_merged_value(
    status: dict[str, Any] | str,
    value1: Any,
    value2: Any,
) -> dict[str, Any]:
    if isinstance(status, dict):
        return merge_dicts(diff=status, dict1=value1, dict2=value2)

    if status == CHANGED:
        return {"status": "changed", "before": value1, "after": value2}

    if status == DELETED:
        return {"status": status, "value": value1}

    return {"status": status, "value": value2}
