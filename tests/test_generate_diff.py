import gendiff
import pytest
from gendiff.format import json_format, plain, stylish


@pytest.mark.parametrize(
    "answer_path, file1_path, file2_path",
    [
        [
            "answers/stylish_plain_plain.txt",
            "json/plain1.json",
            "json/plain2.json",
        ],
        [
            "answers/stylish_empty_empty.txt",
            "json/empty.json",
            "json/empty.json",
        ],
        [
            "answers/stylish_plain_empty.txt",
            "json/plain1.json",
            "json/empty.json",
        ],
        [
            "answers/stylish_plain_plain.txt",
            "yaml/plain1.yml",
            "yaml/plain2.yml",
        ],
        [
            "answers/stylish_empty_empty.txt",
            "yaml/empty.yaml",
            "yaml/empty.yaml",
        ],
        [
            "answers/stylish_plain_empty.txt",
            "yaml/plain1.yml",
            "yaml/empty.yaml",
        ],
        [
            "answers/stylish_recursive.txt",
            "json/recursive1.json",
            "json/recursive2.json",
        ],
        [
            "answers/stylish_recursive.txt",
            "yaml/recursive1.yml",
            "yaml/recursive2.yml",
        ],
    ]
)
def test_stylish(prepare_data, answer_path, file1_path, file2_path):
    answer, file1, file2 = prepare_data(answer_path, file1_path, file2_path)
    assert gendiff.generate_diff(file1, file2, stylish.stylish) == answer


@pytest.mark.parametrize(
    "answer_path, file1_path, file2_path",
    [
        [
            "answers/plain_plain_plain.txt",
            "json/plain1.json",
            "json/plain2.json",
        ],
        [
            "answers/plain_empty_empty.txt",
            "json/empty.json",
            "json/empty.json",
        ],
        [
            "answers/plain_plain_empty.txt",
            "json/plain1.json",
            "json/empty.json",
        ],
        [
            "answers/plain_plain_plain.txt",
            "yaml/plain1.yml",
            "yaml/plain2.yml",
        ],
        [
            "answers/plain_empty_empty.txt",
            "yaml/empty.yaml",
            "yaml/empty.yaml",
        ],
        [
            "answers/plain_plain_empty.txt",
            "yaml/plain1.yml",
            "yaml/empty.yaml",
        ],
        [
            "answers/plain_recursive.txt",
            "json/recursive1.json",
            "json/recursive2.json",
        ],
        [
            "answers/plain_recursive.txt",
            "yaml/recursive1.yml",
            "yaml/recursive2.yml",
        ],
    ]
)
def test_plain(prepare_data, answer_path, file1_path, file2_path):
    answer, file1, file2 = prepare_data(answer_path, file1_path, file2_path)
    assert gendiff.generate_diff(file1, file2, plain.plain) == answer


@pytest.mark.parametrize(
    "answer_path, file1_path, file2_path",
    [
        [
            "answers/json_plain_plain.txt",
            "json/plain1.json",
            "json/plain2.json",
        ],
        [
            "answers/json_empty_empty.txt",
            "json/empty.json",
            "json/empty.json",
        ],
        [
            "answers/json_plain_empty.txt",
            "json/plain1.json",
            "json/empty.json",
        ],
        [
            "answers/json_plain_plain.txt",
            "yaml/plain1.yml",
            "yaml/plain2.yml",
        ],
        [
            "answers/json_empty_empty.txt",
            "yaml/empty.yaml",
            "yaml/empty.yaml",
        ],
        [
            "answers/json_plain_empty.txt",
            "yaml/plain1.yml",
            "yaml/empty.yaml",
        ],
        [
            "answers/json_recursive.txt",
            "json/recursive1.json",
            "json/recursive2.json",
        ],
        [
            "answers/json_recursive.txt",
            "yaml/recursive1.yml",
            "yaml/recursive2.yml",
        ],
    ]
)
def test_json(prepare_data, answer_path, file1_path, file2_path):
    answer, file1, file2 = prepare_data(answer_path, file1_path, file2_path)
    result = gendiff.generate_diff(file1, file2, json_format.json_format)
    assert result == answer


def test_not_found_error(update_path):
    file1, file2 = update_path("json/plain1.json", "json/plain.json")
    with pytest.raises(FileNotFoundError):
        gendiff.generate_diff(file1, file2)


def test_incorrect_files(update_path):
    file1 = "png/incorrect_format_1.png"
    file2 = "png/incorrect_format_2.png"
    file1, file2 = update_path(file1, file2)
    with pytest.raises(ValueError) as e:
        gendiff.generate_diff(file1, file2)
    assert str(e.value) == "ERROR: Files have incorrect extension"


@pytest.mark.parametrize(
    "file1, file2",
    [
        ["json/plain1.json", "json/invalid.json"],
        ["yaml/plain1.yml", "yaml/invalid.yml"],
    ]
)
def test_encoder_error(update_path, file1, file2):
    file1, file2 = update_path(file1, file2)
    with pytest.raises(ValueError) as e:
        gendiff.generate_diff(file1, file2)
    assert str(e.value) == "ERROR: Files contain invalid data"
