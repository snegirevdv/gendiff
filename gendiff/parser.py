import json
from typing import Any

import yaml
from gendiff import constants as const


def parse_data_from_files(
    file1_path: str,
    file2_path: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        if (
            file1_path.endswith(const.JSON_FORMATS)
            and file2_path.endswith(const.JSON_FORMATS)
        ):
            return (
                parse_json_from_file(file1_path),
                parse_json_from_file(file2_path)
            )
        if (
            file1_path.endswith(const.YAML_FORMATS)
            and file2_path.endswith(const.YAML_FORMATS)
        ):
            return (
                parse_yaml_from_file(file1_path),
                parse_yaml_from_file(file2_path)
            )
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
