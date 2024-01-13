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
    merged_jsons = merge_dicts(json1, json2)
    return get_diff_report(merged_jsons)


def merge_dicts(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
) -> dict[tuple, Any]:
    merged = {}
    keys = set(dict1) | set(dict2)

    for key in keys:
        first_has_key = key in dict1
        second_has_key = key in dict2
        both_have_key = first_has_key and second_has_key
        are_equal = dict1.get(key) == dict2.get(key)

        if not first_has_key or both_have_key and not are_equal:
            merged[(key, 1)] = convert_value(dict2[key])
        if not second_has_key or both_have_key and not are_equal:
            merged[(key, -1)] = convert_value(dict1[key])
        if both_have_key and are_equal:
            merged[(key, 0)] = convert_value(dict1[key])

    return merged


def convert_value(value: Any) -> Any:
    return JSON_VALUE_CONVERTER.get(value) or value


def get_diff_report(data: dict) -> str:
    result = "{\n"
    for key_tuple, value in sorted(data.items()):
        key, prefix_key = key_tuple
        line = f"{LINE_PREFIX_VALUES[prefix_key]}{key}: {value}\n"
        result += line
    result += "}"
    return result
