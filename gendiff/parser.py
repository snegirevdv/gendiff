import json
from typing import Any

import yaml
from gendiff import constants as const


def parse_data_from_files(
    file1: str,
    file2: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Parse data from two files and return their content as dictionaries.
    Supports JSON and YAML file formats.

    Raises:
        FileNotFoundError: If either of the files does not exist.
        ValueError: If file formats are not supported or contain invalid data.
    """
    try:
        if (
            file1.endswith(const.JSON_FORMATS)
            and file2.endswith(const.JSON_FORMATS)
        ):
            return parse_json_from_file(file1), parse_json_from_file(file2)
        if (
            file1.endswith(const.YAML_FORMATS)
            and file2.endswith(const.YAML_FORMATS)
        ):
            return parse_yaml_from_file(file1), parse_yaml_from_file(file2)
        raise ValueError(const.EXTENSION_ERROR)
    except FileNotFoundError:
        raise FileNotFoundError(const.NOT_FOUND_ERROR)


def parse_json_from_file(filename: str) -> dict[str, Any]:
    with open(filename) as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            raise ValueError(const.INVALID_ERROR)


def parse_yaml_from_file(filename) -> dict[str, Any]:
    with open(filename) as file:
        try:
            data = yaml.safe_load(file)
            if data is not None:
                return data
            return {}
        except (yaml.YAMLError, KeyError):
            raise ValueError(const.INVALID_ERROR)
