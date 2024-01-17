import json
from typing import Any

from gendiff.format import utils


def get_view(diff: dict[str, dict[str, Any]]) -> str:
    diff = utils.get_sorted_diff(diff)
    return json.dumps(diff, indent=3)
