import json
from collections.abc import Callable, Hashable
from typing import Any

import yaml
from gendiff.constants import (
    EXTENSION_ERROR,
    INVALID_ERROR,
    JSON_FORMATS,
    NOT_FOUND_ERROR,
    YAML_FORMATS,
)


def parse_data_from_files(file1: str, file2: str) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        if file1.endswith(JSON_FORMATS) and file2.endswith(JSON_FORMATS):
            return parse_json_from_file(file1), parse_json_from_file(file2)
        if file1.endswith(YAML_FORMATS) and file2.endswith(YAML_FORMATS):
            return parse_yaml_from_file(file1), parse_yaml_from_file(file2)
        raise ValueError(EXTENSION_ERROR)
    except FileNotFoundError:
        raise FileNotFoundError(NOT_FOUND_ERROR)


def parse_json_from_file(filename: str) -> dict[str, Any]:
    with open(filename) as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            raise ValueError(INVALID_ERROR)


def parse_yaml_from_file(filename) -> dict[str, Any]:
    with open(filename) as file:
        try:
            data = yaml.safe_load(file)
            if data is not None:
                return data
            return {}
        except (yaml.YAMLError, KeyError):
            raise ValueError(INVALID_ERROR)
