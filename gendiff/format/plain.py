from typing import Any

from gendiff import constants as const
from gendiff.format import constants as fconst
from gendiff.format import utils


def get_view(diff: dict, prefix: str = "") -> str:
    """
    Format the diff into a plain text report.

    Args:
        diff: diff dictionary.
        dict1, dict2: compared dictionaries.
        prefix (optional): current prefix of the file name. Default: "".

    Returns:
        Formatted diff view.
    """
    diff = utils.get_sorted_diff(diff)
    view = ""

    for key, diff_entry in diff.items():
        if isinstance(diff_entry, dict):
            new_prefix = prefix + key + fconst.DELIMETER
            view += get_view(diff=diff_entry, prefix=new_prefix)

        elif diff_entry[0] != const.UNCHANGED:
            view += get_line(key, diff_entry, prefix)

    if not prefix:
        view = view.rstrip()

    return view


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
    return f"'{value}'"
