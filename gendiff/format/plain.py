from typing import Any

from gendiff import constants as const
from gendiff.format import constants as fconst
from gendiff.format import utils


def get_view(diff: dict, prefix: str = "") -> str:
    diff = utils.get_sorted_diff(diff)
    view = "".join(make_block(key, diff, prefix) for key in diff.keys())

    if not prefix:
        return view.rstrip()

    return view


def make_block(key, diff, prefix):
    diff_entry = diff[key]

    if isinstance(diff_entry, dict):
        new_prefix = prefix + key + fconst.DELIMETER
        return get_view(diff_entry, new_prefix)

    if diff_entry[0] != const.UNCHANGED:
        return get_line(key, diff_entry, prefix)

    return ""


def get_line(key: str, diff_entry: dict[str, Any], prefix: str) -> str:
    status = diff_entry[0]
    values = tuple(map(update_value, diff_entry[1:]))

    message = fconst.MESSAGES[status].format(values=values)

    return f"{fconst.PROPERTY} '{prefix}{key}' {message}\n"


def update_value(value: Any) -> str:
    if isinstance(value, dict):
        return fconst.COMPLEX
    if value is None or isinstance(value, bool):
        return fconst.VALUE_CONVERTOR[value]
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)
