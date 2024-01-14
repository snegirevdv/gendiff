import json
from collections.abc import Callable, Hashable
from typing import Any

import yaml

JSON_VALUE_CONVERTER = {
    True: "true",
    False: "false",
    None: "null",
}

LINE_PREFIX_VALUES = {
    -1: "-",
    0: " ",
    1: "+",
}


def generate_diff(file1: str, file2: str) -> str:
    dict1, dict2 = load_data(file1, file2)
    merged_data = merge_dicts(dict1, dict2)
    return get_diff_report(merged_data)


def load_data(file1: str, file2: str) -> Callable:
    try:
        if file1.endswith('json') and file2.endswith('json'):
            return load_json(file1, file2)
        if file1.endswith(('yml', 'yaml')) and file2.endswith(('yml', 'yaml')):
            return load_yaml(file1, file2)
        raise ValueError("ERROR: Files have incorrect extension")
    except FileNotFoundError:
        raise FileNotFoundError("ERROR: File Not Found")


def load_json(
    file1: str,
    file2: str,
) -> tuple[dict[Hashable, Any], dict[Hashable, Any]]:
    with open(file1) as file1, open(file2) as file2:
        try:
            return (json.load(file1), json.load(file2))
        except json.JSONDecodeError:
            raise ValueError("ERROR: Files contain invalid data")


def load_yaml(
    file1: str,
    file2: str,
) -> tuple[dict[Hashable, Any], dict[Hashable, Any]]:
    with open(file1) as file1, open(file2) as file2:
        try:
            dict1 = yaml.safe_load(file1) or {}
            dict2 = yaml.safe_load(file2) or {}
            return (dict1, dict2)
        except (yaml.YAMLError, KeyError):
            raise ValueError("ERROR: Files contain invalid data")


def merge_dicts(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[tuple[Hashable, int], Any]:
    merged = {}

    keys_1 = set(dict1)
    keys_2 = set(dict2)

    unchanged_keys = set(
        filter(lambda key: dict1[key] == dict2[key], keys_1 & keys_2)
    )
    changed_keys = set(
        filter(lambda key: dict1[key] != dict2[key], keys_1 & keys_2)
    )
    deleted_keys = keys_1 - keys_2
    added_keys = keys_2 - keys_1

    for key in unchanged_keys:
        merged[(key, 0)] = convert_value(dict1[key])

    for key in deleted_keys | changed_keys:
        merged[(key, -1)] = convert_value(dict1[key])

    for key in added_keys | changed_keys:
        merged[(key, 1)] = convert_value(dict2[key])

    return merged


def convert_value(value: Any) -> Any:
    return JSON_VALUE_CONVERTER.get(value) or value


def get_diff_report(data: dict) -> str:
    result = "{\n"
    for key_tuple, value in sorted(data.items()):
        key, prefix_key = key_tuple
        line = f"  {LINE_PREFIX_VALUES[prefix_key]} {key}: {value}\n"
        result += line
    result += "}"
    return result
