from typing import Any

from gendiff import constants as const
from gendiff.format import constants as fconst
from gendiff.format import utils


def get_view(
    diff: dict[str, dict[str, Any]],
    step: int = 0,
) -> str:
    """
    Format the diff into a stylish, JSON-like style.
    Changes marked by "+" (added) and "-" (deleted).

    Args:
        diff: the diff dictionary.
        step (optional): the current indentation level. Default: 0.

    Returns:
        Formatted diff view.
    """
    diff = utils.get_sorted_diff(diff)
    view = fconst.START_LINE

    for key, diff_entry in diff.items():
        view += get_block(key, diff_entry, step)

    view += get_indent(step) + fconst.FINISH_LINE

    if not step:
        view = view.rstrip()

    return view


def get_block(
    key: str,
    diff_entry: list[Any] | dict[str, Any],
    step: int,
) -> str:
    if isinstance(diff_entry, dict):
        return get_left(key, step) + get_view(diff_entry, step + 1)

    status, *diff_values = diff_entry

    if status == const.CHANGED:
        return get_changed_block(key, diff_values, step)

    return get_left(key, step, status) + get_right(*diff_values, step)


def get_changed_block(key, diff_values, step):
    before, after = diff_values
    first = get_left(key, step, const.DELETED) + get_right(before, step)
    second = get_left(key, step, const.ADDED) + get_right(after, step)
    return first + second


def get_left(
    key: str,
    step: int,
    status: str = const.UNCHANGED,
    subdict: bool = False,
) -> str:
    if subdict:
        return f"{get_indent(step + 1)}{key}: "
    return f"{get_indent(step)}  {fconst.PREFIXES[status]} {key}: "


def get_right(diff_value: Any, step: int) -> str:
    if isinstance(diff_value, dict):
        block = fconst.START_LINE

        for sub_key in diff_value:
            block += get_left(sub_key, step + 1, subdict=True)
            block += get_right(diff_value[sub_key], step + 1)

        block += get_indent(step + 1) + fconst.FINISH_LINE

        return block

    return update_value(diff_value) + "\n"


def get_indent(step: int) -> str:
    return f"{fconst.INDENT_SYMBOL * fconst.INDENT_SIZE * step}"


def update_value(value: Any) -> str:
    if value is None or isinstance(value, bool):
        return fconst.VALUE_CONVERTOR[value]
    return str(value)
