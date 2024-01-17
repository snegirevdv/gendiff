import json
from typing import Any

from gendiff.format import utils


def get_view(diff: dict[str, dict[str, Any]]) -> str:
    """
    Format the diff dictionary into a standart JSON.

    Args:
        diff: diff dictionary.

    Returns:
        Formatted diff view.
    """
    diff = utils.get_sorted_diff(diff)
    return json.dumps(diff, indent=3)
