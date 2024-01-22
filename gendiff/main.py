from typing import Callable

from gendiff import constants as const
from gendiff import diff, parser
from gendiff.format import json_format, plain, stylish

FORMATTERS = {
    const.STYLISH: stylish.get_view,
    const.PLAIN: plain.get_view,
    const.JSON: json_format.get_view,
}


def generate_diff(
    file1_path: str,
    file2_path: str,
    format: str = const.STYLISH
) -> str:
    """
    Generate a textual formatted diff report between two files.

    Args:
        file1_path: Path to the first file to compare.
        file2_path: Path to the second file to compare.
        formatter (optional): Function to format the diff output.

    Formatter Options:
        stylish (default): JSON-like format, changes marked by "+" and "-".
        plain: textual report of changes, shows property updates.
        json_format: standard JSON format representation.
    """
    parsed_data = parser.parse_data_from_files(file1_path, file2_path)
    diffs = diff.get_diffs(*parsed_data)
    formatter = get_formatter(format)

    return formatter(diffs)


def get_formatter(format: str) -> Callable:
    return FORMATTERS[format]
