import json
from collections.abc import Callable, Hashable
from typing import Any

import yaml
from gendiff.constants import ERRORS, FORMATS


def parse_data(file1: str, file2: str) -> Callable:
    try:
        if file1.endswith(FORMATS["JSON"]) and file2.endswith(FORMATS["JSON"]):
            return parse_json(file1), parse_json(file2)
        if file1.endswith(FORMATS["YAML"]) and file2.endswith(FORMATS["YAML"]):
            return parse_yaml(file1), parse_yaml(file2)
        raise ValueError(ERRORS["extension"])
    except FileNotFoundError:
        raise FileNotFoundError(ERRORS["not_found"])


def parse_json(filename: str) -> dict[Hashable, Any]:
    with open(filename) as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            raise ValueError(ERRORS["invalid"])


def parse_yaml(filename) -> dict[Hashable, Any]:
    with open(filename) as file:
        try:
            data = yaml.safe_load(file)
            if data is not None:
                return data
            return {}
        except (yaml.YAMLError, KeyError):
            raise ValueError(ERRORS["invalid"])
