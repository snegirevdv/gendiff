import json
from typing import Any


def get_view(diff: dict[str, dict[str, Any]]) -> str:
    result = json.dumps(diff, indent=3)
    with open("json_.txt", "w") as file:
        file.write(result)
    return json.dumps(diff, indent=3)
