from typing import Any

from gendiff.constants import ADDED, CHANGED, DELETED, UNCHANGED
from gendiff.format.constants import (
    FINISH_LINE,
    INDENT_SIZE,
    INDENT_SYMBOL,
    PREFIXES,
    START_LINE,
    VALUE_CONVERTOR,
)


def stylish(
    diff: dict[str, str],
    dict1: dict[str, Any],
    dict2: dict[str, Any],
    step: int = 0,
) -> str:
    """
    Format the diff in a JSON-like style with marked changed strings.

    Args:
        diff: diff dictionary.
        dict1, dict2: compared dictionaries.
        step (optional): current indentation level. Default: 0.

    Returns:
        Formatted diff view.
    """
    view = START_LINE

    for items in sorted(diff.items()):
        key, _ = items
        value1, value2 = dict1.get(key), dict2.get(key)
        view += get_block(items, value1, value2, step)

    view += get_indent(step) + FINISH_LINE

    if not step:
        view = view.rstrip()

    return view


def get_block(
    items: tuple[str, str],
    value1: Any,
    value2: Any,
    step: int,
) -> str:
    key, status = items

    if isinstance(status, dict):
        left = get_left(key, step)
        right = stylish(diff=status, dict1=value1, dict2=value2, step=step + 1)
        return left + right

    if status == UNCHANGED:
        return get_left(key, step) + get_right(value2, step + 1)

    return accumulate_lines(items, value1, value2, step)


def accumulate_lines(
    items: tuple[str, str],
    value1: Any,
    value2: Any,
    step: int,
) -> str:
    key, status = items
    block = ""

    if status in (DELETED, CHANGED):
        block += get_left(key, step, DELETED) + get_right(value1, step + 1)

    if status in (ADDED, CHANGED):
        block += get_left(key, step, ADDED) + get_right(value2, step + 1)

    return block


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
        result = START_LINE
        for sub_key in value:
            result += get_left(key=sub_key, step=step + 1, subdict=True)
            result += get_right(value=value[sub_key], step=step + 1)
        result += get_indent(step) + FINISH_LINE
        return result
    return update_value(value) + "\n"


def get_indent(step: int) -> str:
    return f"{INDENT_SYMBOL * step * INDENT_SIZE}"


def update_value(value: Any) -> str:
    return VALUE_CONVERTOR.get(value, str(value))
