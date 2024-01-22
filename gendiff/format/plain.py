from typing import Any

from gendiff import constants as const, diff
from gendiff.format import constants as fconst


def get_view(diffs: list[dict[str, Any]], prefix: str = "") -> str:
    view: str = "".join(make_block(diff_item, prefix) for diff_item in diffs)

    if not prefix:
        return view.rstrip()

    return view


def make_block(diff_item: dict[str, Any], prefix: str) -> str:
    key = diff.get_key(diff_item)
    status = diff.get_status(diff_item)

    if status == const.NESTED:
        new_prefix = prefix + key + fconst.DELIMETER
        elements = diff.get_nested_elements(diff_item)
        return get_view(elements, new_prefix)

    if status != const.UNCHANGED:
        return make_line(diff_item, prefix)

    return ""


def make_line(diff_item: dict[str, Any], prefix: str) -> str:
    key = diff.get_key(diff_item)
    status = diff.get_status(diff_item)

    if status == const.CHANGED:
        before, after = diff.get_changed_values(diff_item)
        upd_before, upd_after = update_value(before), update_value(after)
        message = get_message(status, upd_before, upd_after)

    else:
        upd_value = update_value(diff.get_value(diff_item))
        message = get_message(status, upd_value)

    return f"{fconst.PROPERTY} '{prefix}{key}' {message}\n"


def update_value(value: Any) -> str:
    if isinstance(value, dict):
        return fconst.COMPLEX

    if value is None or isinstance(value, bool):
        return fconst.VALUE_CONVERTOR[value]

    if isinstance(value, str):
        return f"'{value}'"

    return str(value)


def get_message(status, *values):
    return fconst.MESSAGES[status].format(*values)
