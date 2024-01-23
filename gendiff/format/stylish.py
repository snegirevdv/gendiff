from typing import Any

from gendiff import consts, diff
from gendiff.format import consts as fconsts


def render_view(diffs: list[dict[str, Any]], step: int = 0) -> str:
    view = fconsts.START_LINE
    view += "".join(make_item_block(diff_item, step) for diff_item in diffs)
    view += make_indent(step) + fconsts.FINISH_LINE

    if not step:
        return view.rstrip()

    return view


def make_item_block(diff_item: dict[str, Any], step: int) -> str:
    key = diff.get_key(diff_item)
    status = diff.get_status(diff_item)

    if status == consts.NESTED:
        elements = diff.get_nested_elements(diff_item)
        return make_left_part(key, step) + render_view(elements, step + 1)

    if status == consts.CHANGED:
        before_value, after_value = diff.get_changed_values(diff_item)
        first_line = (make_left_part(key, step, status=consts.DELETED)
                      + make_right_part(before_value, step))
        second_line = (make_left_part(key, step, status=consts.ADDED)
                       + make_right_part(after_value, step))
        return first_line + second_line

    value = diff.get_value(diff_item)
    return make_left_part(key, step, status) + make_right_part(value, step)


def make_left_part(key: str, step: int, status: str = consts.UNCHANGED) -> str:
    return f"{make_indent(step)}{make_prefix(status)}{key}: "


def make_right_part(value: Any, step: int) -> str:
    if isinstance(value, dict):
        return make_subdict_view(value, step + 1)
    return stringify_value(value) + "\n"


def make_subdict_view(subdict: dict[str, Any], step) -> str:
    view = fconsts.START_LINE

    for key in subdict:
        value = subdict[key]
        view += make_left_part(key, step) + make_right_part(value, step)

    view += make_indent(step) + fconsts.FINISH_LINE

    return view


def stringify_value(value: Any) -> str:
    if value is None or isinstance(value, bool):
        return fconsts.VALUE_CONVERTOR[value]
    return str(value)


def make_indent(step: int) -> str:
    return f"{fconsts.SPACE * fconsts.INDENT_SIZE * step}"


def make_prefix(status: str) -> str:
    return fconsts.SPACE * 2 + fconsts.PREFIXES[status] + fconsts.SPACE
