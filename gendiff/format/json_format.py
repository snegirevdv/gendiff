import json
from typing import Any

from gendiff.format import utils


def get_view(diff: dict[str, dict[str, Any]]) -> str:
    """
    Format the diff in a standard JSON style.

    Args:
        diff: diff dictionary.
        dict1, dict2: compared dictionaries.

    Returns:
        Formatted diff view.
    """
    diff = utils.get_sorted_diff(diff)
    return json.dumps(diff, indent=3)
