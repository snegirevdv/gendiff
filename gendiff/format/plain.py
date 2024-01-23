from typing import Any

from gendiff import consts, diff
from gendiff.format import consts as fconsts


def render_view(diffs: list[dict[str, Any]], prefix: str = "") -> str:
    view = "".join(make_item_block(diff_item, prefix) for diff_item in diffs)

    if not prefix:
        return view.rstrip()

    return view


def make_item_block(diff_item: dict[str, Any], prefix: str) -> str:
    key = diff.get_key(diff_item)
    status = diff.get_status(diff_item)

    if status == consts.NESTED:
        new_prefix = prefix + key + fconsts.DELIMETER
        elements = diff.get_nested_elements(diff_item)
        return render_view(elements, new_prefix)

    if status == consts.UNCHANGED:
        return ""

    if status == consts.CHANGED:
        before_value, after_value = diff.get_changed_values(diff_item)
        upd_before_value = stringify_value(before_value)
        upd_after_value = stringify_value(after_value)
        message = get_message(status, upd_before_value, upd_after_value)

    else:
        upd_value = stringify_value(diff.get_value(diff_item))
        message = get_message(status, upd_value)

    return f"{fconsts.PROPERTY} '{prefix}{key}' {message}\n"


def stringify_value(value: Any) -> str:
    if isinstance(value, dict):
        return fconsts.COMPLEX

    if value is None or isinstance(value, bool):
        return fconsts.VALUE_CONVERTOR[value]

    if isinstance(value, str):
        return f"'{value}'"

    return str(value)


def get_message(status, *values):
    return fconsts.MESSAGES[status].format(*values)
