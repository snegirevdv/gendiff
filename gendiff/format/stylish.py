from typing import Any

from gendiff.constants import (
    ADDED,
    AFTER,
    BEFORE,
    CHANGED,
    DELETED,
    NESTED,
    STATUS,
    UNCHANGED,
    VALUE,
)
from gendiff.format.constants import (
    FINISH_LINE,
    INDENT_SIZE,
    INDENT_SYMBOL,
    PREFIXES,
    START_LINE,
    VALUE_CONVERTOR,
)


def stylish(
    diff: dict[str, dict[str, Any]],
    step: int = 0,
) -> str:
    """
    Format the diff in a JSON-like style with marked changed strings.

    Args:
        diff: diff dictionary.
        step (optional): current indentation level. Default: 0.

    Returns:
        Formatted diff view.
    """
    view = START_LINE

    for key, item in diff.items():
        view += get_block(key, item, step)

    view += get_indent(step) + FINISH_LINE

    if not step:
        view = view.rstrip()

    return view


def get_block(key: str, item: dict[str, Any], step: int) -> str:
    status = item[STATUS]

    if status == NESTED:
        new_diff = item[VALUE]
        left = get_left(key, step)
        right = stylish(diff=new_diff, step=step + 1)
        return left + right

    if status == CHANGED:
        return get_changed_block(key, item, step)

    value = item[VALUE]

    return get_left(key, step, status) + get_right(value, step + 1)


def get_changed_block(key, item, step):
    before = item[BEFORE]
    after = item[AFTER]
    first = get_left(key, step, DELETED) + get_right(before, step + 1)
    second = get_left(key, step, ADDED) + get_right(after, step + 1)
    return first + second


def get_left(
    key: str,
    step: int,
    status: str = UNCHANGED,
    subdict: bool = False,
) -> str:
    if subdict:
        return f"{get_indent(step)}{key}: "
    return f"{get_indent(step)}  {PREFIXES[status]} {key}: "


def get_right(value: Any, step: int) -> str:
    if isinstance(value, dict):
        block = START_LINE

        for sub_key in value:
            block += get_left(key=sub_key, step=step + 1, subdict=True)
            block += get_right(value=value[sub_key], step=step + 1)

        block += get_indent(step) + FINISH_LINE

        return block

    return update_value(value) + "\n"


def get_indent(step: int) -> str:
    return f"{INDENT_SYMBOL * step * INDENT_SIZE}"


def update_value(value: Any) -> str:
    return VALUE_CONVERTOR.get(value, str(value))
