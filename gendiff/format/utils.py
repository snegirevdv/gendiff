from typing import Any


def get_sorted_diff(diff: dict[str, Any]) -> dict[str, Any]:
    sorted_diff = {}
    for key, value in sorted(diff.items()):
        if isinstance(value, dict):
            sorted_diff[key] = get_sorted_diff(value)
        else:
            sorted_diff[key] = value

    return sorted_diff
