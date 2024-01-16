from typing import Any

from gendiff.constants import UNCHANGED
from gendiff.format.constants import (
    COMPLEX,
    DELIMETER,
    MESSAGES,
    PROPERTY,
    VALUE_CONVERTOR,
)


def plain(diff: dict, dict1: dict, dict2: dict, prefix: str = "") -> str:
    view = ""

    for items in sorted(diff.items()):
        key, status = items
        value1, value2 = dict1.get(key), dict2.get(key)
        if status != UNCHANGED:
            view += get_line(items, value1, value2, prefix)

    if not prefix:
        view = view.rstrip()

    return view


def get_line(items: tuple, value1: Any, value2: Any, prefix: str) -> str:
    key, status = items

    if isinstance(value1, dict) and isinstance(value2, dict):
        new_prefix = prefix + key + DELIMETER
        return plain(diff=status, dict1=value1, dict2=value2, prefix=new_prefix)

    value1 = update_value(value1)
    value2 = update_value(value2)

    message = MESSAGES[status].format(before=value1, after=value2)

    return f"{PROPERTY} '{prefix}{key}' {message}\n"


def update_value(value: Any) -> str:
    if isinstance(value, dict):
        return COMPLEX
    return VALUE_CONVERTOR.get(value, f"'{value}'")
