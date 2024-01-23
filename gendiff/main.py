from typing import Callable

from gendiff import consts, diff, parser
from gendiff.format import json_format, plain, stylish

FORMATTERS = {
    consts.STYLISH: stylish.render_view,
    consts.PLAIN: plain.render_view,
    consts.JSON: json_format.render_view,
}


def generate_diff(
    file_path_1: str,
    file_path_2: str,
    format: str = consts.DEFAULT_FORMAT,
) -> str:
    """
    Generate a textual formatted diff report between two files.

    Args:
        file_path_1: Path to the first file to compare.
        file_path_2: Path to the second file to compare.
        formatter (optional): Function to format the diff output.

    Formatter Options:
        stylish (default): JSON-like format, changes marked by "+" and "-".
        plain: textual report of changes, shows property updates.
        json_format: standard JSON format representation.
    """
    parsed_data = parser.parse_data_from_files(file_path_1, file_path_2)
    diffs = diff.get_diffs(*parsed_data)
    formatter = get_formatter(format)

    return formatter(diffs)


def get_formatter(format: str) -> Callable:
    try:
        return FORMATTERS[format]
    except KeyError:
        return FORMATTERS[consts.DEFAULT_FORMAT]
