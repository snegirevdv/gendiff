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
        left = get_left(key, step)
        right = get_view(diff=diff_entry, step=step + 1)
        return left + right

    status = diff_entry[0]

    if status == const.CHANGED:
        return get_changed_block(key, diff_entry[1:], step)

    diff_value = diff_entry[1]

    return get_left(key, step, status) + get_right(diff_value, step + 1)


def get_changed_block(key, diff_entry, step):
    before, after = diff_entry
    first = get_left(key, step, const.DELETED) + get_right(before, step + 1)
    second = get_left(key, step, const.ADDED) + get_right(after, step + 1)
    return first + second


def get_left(
    key: str,
    step: int,
    status: str = const.UNCHANGED,
    subdict: bool = False,
) -> str:
    if subdict:
        return f"{get_indent(step)}{key}: "
    return f"{get_indent(step)}  {fconst.PREFIXES[status]} {key}: "


def get_right(diff_value: Any, step: int) -> str:
    if isinstance(diff_value, dict):
        block = fconst.START_LINE

        for sub_key in diff_value:
            block += get_left(key=sub_key, step=step + 1, subdict=True)
            block += get_right(diff_value=diff_value[sub_key], step=step + 1)

        block += get_indent(step) + fconst.FINISH_LINE

        return block

    return update_value(diff_value) + "\n"


def get_indent(step: int) -> str:
    return f"{fconst.INDENT_SYMBOL * step * fconst.INDENT_SIZE}"


def update_value(value: Any) -> str:
    if value is None or isinstance(value, bool):
        return fconst.VALUE_CONVERTOR[value]
    return str(value)
