from typing import Any


def get_sorted_diff(diff: dict[str, Any]) -> dict[str, Any]:
    sorted_diff = {}
    for key, diff_value in sorted(diff.items()):
        if isinstance(diff_value, dict):
            sorted_diff[key] = get_sorted_diff(diff_value)
        else:
            sorted_diff[key] = diff_value

    return sorted_diff
