import json
from typing import Any

JSON_VALUE_CONVERTER = {
    True: "true",
    False: "false",
    None: "null",
}

LINE_PREFIX_VALUES = {
    -1: "  - ",
    0: "    ",
    1: "  + ",
}


def generate_diff(file1: str, file2: str) -> str:
    try:
        with open(file1) as file1, open(file2) as file2:
            try:
                json1: dict = json.load(file1)
                json2: dict = json.load(file2)
            except json.JSONDecodeError:
                raise ValueError("ERROR: Files contain invalid data")
    except FileNotFoundError:
        raise FileNotFoundError("ERROR: File Not Found")
    merged_jsons = merge_dicts_and_convert_values(json1, json2)
    return get_diff_report(merged_jsons)


def merge_dicts_and_convert_values(
    dict1: dict,
    dict2: dict
) -> dict[tuple, Any]:
    keys = set(dict1) | set(dict2)
    result = {}
    for key in keys:
        if key not in dict1:
            result[(key, 1)] = convert_value(dict2[key])
        elif key not in dict2:
            result[(key, -1)] = convert_value(dict1[key])
        elif dict1[key] == dict2[key]:
            result[(key, 0)] = convert_value(dict1[key])
        else:
            result[(key, -1)] = convert_value(dict1[key])
            result[(key, 1)] = convert_value(dict2[key])
    return result


def get_diff_report(data: dict) -> str:
    result = "{\n"
    for key_tuple, value in sorted(data.items()):
        key, prefix_key = key_tuple
        line = f"{LINE_PREFIX_VALUES[prefix_key]}{key}: {value}\n"
        result += line
    result += "}"
    return result


def convert_value(value: Any) -> Any:
    return JSON_VALUE_CONVERTER.get(value) or value
