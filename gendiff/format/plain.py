from typing import Any

from gendiff.constants import AFTER, BEFORE, NESTED, STATUS, UNCHANGED, VALUE
from gendiff.format.constants import (
    COMPLEX,
    DELIMETER,
    MESSAGES,
    PROPERTY,
    VALUE_CONVERTOR,
)


def plain(diff: dict, prefix: str = "") -> str:
    """
    Format the diff as a textual changes report.

    Args:
        diff: diff dictionary.
        dict1, dict2: compared dictionaries.
        prefix (optional): current prefix of the file name. Default: "".

    Returns:
        Formatted diff view.
    """
    view = ""

    for key, item in diff.items():
        status = item[STATUS]

        if status != UNCHANGED:
            view += get_line(key, item, status, prefix)

    if not prefix:
        view = view.rstrip()

    return view


def get_line(key: str, item: dict[str, Any], status: str, prefix: str) -> str:
    if status == NESTED:
        new_prefix = prefix + key + DELIMETER
        return plain(diff=item[VALUE], prefix=new_prefix)

    value, before, after = item.get(VALUE), item.get(BEFORE), item.get(AFTER)

    value = update_value(value)
    before = update_value(before)
    after = update_value(after)

    message = MESSAGES[status].format(before=before, after=after, value=value)

    return f"{PROPERTY} '{prefix}{key}' {message}\n"


def update_value(value: Any) -> str:
    if isinstance(value, dict):
        return COMPLEX
    return VALUE_CONVERTOR.get(value, f"'{value}'")
