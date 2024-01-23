import json
from typing import Any

import yaml
from gendiff import consts


def parse_data_from_files(
    file_path_1: str,
    file_path_2: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        if (
            file_path_1.endswith(consts.JSON_FORMATS)
            and file_path_2.endswith(consts.JSON_FORMATS)
        ):
            return (
                parse_json_from_file(file_path_1),
                parse_json_from_file(file_path_2)
            )
        if (
            file_path_1.endswith(consts.YAML_FORMATS)
            and file_path_2.endswith(consts.YAML_FORMATS)
        ):
            return (
                parse_yaml_from_file(file_path_1),
                parse_yaml_from_file(file_path_2)
            )
        raise ValueError(consts.EXTENSION_ERROR)
    except FileNotFoundError as e:
        raise FileNotFoundError(consts.NOT_FOUND_ERROR) from e


def parse_json_from_file(file_path: str) -> dict[str, Any]:
    with open(file_path) as file:
        try:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError(consts.INVALID_ERROR)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(consts.INVALID_ERROR) from e


def parse_yaml_from_file(file_path: str) -> dict[str, Any]:
    with open(file_path) as file:
        try:
            data = yaml.safe_load(file)
            if data is not None:
                return data
            return {}
        except (yaml.YAMLError, KeyError) as e:
            raise ValueError(consts.INVALID_ERROR) from e
