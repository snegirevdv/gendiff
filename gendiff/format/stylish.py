from typing import Any

from gendiff import constants as const, diff
from gendiff.format import constants as fconst


def get_view(diffs: list[dict[str, Any]], step: int = 0) -> str:
    view = fconst.START_LINE
    view += "".join(make_block(diff_item, step) for diff_item in diffs)
    view += make_indent(step) + fconst.FINISH_LINE

    if not step:
        view = view.rstrip()

    return view


def make_block(diff_item: dict[str, Any], step: int) -> str:
    status = diff.get_status(diff_item)
    key = diff.get_key(diff_item)

    if status == const.NESTED:
        elements = diff.get_nested_elements(diff_item)
        return make_left(key, step) + get_view(elements, step + 1)

    if status == const.CHANGED:
        before, after = diff.get_changed_values(diff_item)
        first = make_left(key, step, const.DELETED) + make_right(before, step)
        second = make_left(key, step, const.ADDED) + make_right(after, step)
        return first + second

    diff_value = diff.get_value(diff_item)

    return make_left(key, step, status) + make_right(diff_value, step)


def make_left(key: str, step: int, status: str = const.UNCHANGED) -> str:
    return f"{make_indent(step)}{make_prefix(status)}{key}: "


def make_right(diff_value: Any, step: int) -> str:
    if isinstance(diff_value, dict):
        return make_subdict_view(diff_value, step + 1)
    return update_value(diff_value) + "\n"


def make_indent(step: int) -> str:
    return f"{fconst.SPACE * fconst.INDENT_SIZE * step}"


def make_prefix(status: str) -> str:
    return fconst.SPACE * 2 + fconst.PREFIXES[status] + fconst.SPACE


def make_subdict_view(subdict: dict[str, Any], step) -> str:
    view = fconst.START_LINE

    for key in subdict:
        value = subdict[key]
        view += make_left(key, step) + make_right(value, step)

    view += make_indent(step) + fconst.FINISH_LINE

    return view


def update_value(value: Any) -> str:
    if value is None or isinstance(value, bool):
        return fconst.VALUE_CONVERTOR[value]
    return str(value)
