import json
from typing import Any


def get_view(diff: dict[str, dict[str, Any]]) -> str:
    return json.dumps(diff, indent=3)
