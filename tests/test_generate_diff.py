import gendiff
import pytest
from gendiff import consts


@pytest.mark.parametrize(
    "answer_path, file_path_1, file_path_2",
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
    ],
)
def test_stylish_format_success(
    prepare_data,
    answer_path,
    file_path_1,
    file_path_2
):
    answer, file1, file2 = prepare_data(answer_path, file_path_1, file_path_2)
    assert gendiff.generate_diff(file1, file2, consts.STYLISH) == answer


@pytest.mark.parametrize(
    "answer_path, file_path_1, file_path_2",
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
    ],
)
def test_plain_format_success(
    prepare_data,
    answer_path,
    file_path_1,
    file_path_2
):
    answer, file1, file2 = prepare_data(answer_path, file_path_1, file_path_2)
    assert gendiff.generate_diff(file1, file2, consts.PLAIN) == answer


@pytest.mark.parametrize(
    "answer_path, file_path_1, file_path_2",
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
    ],
)
def test_json_format_success(
    prepare_data,
    answer_path,
    file_path_1,
    file_path_2
):
    answer, file1, file2 = prepare_data(answer_path, file_path_1, file_path_2)
    result = gendiff.generate_diff(file1, file2, consts.JSON)
    assert result == answer


def test_parser_not_found_failure(update_path):
    file1, file2 = update_path("json/plain1.json", "json/plain.json")
    with pytest.raises(FileNotFoundError):
        gendiff.generate_diff(file1, file2)


def test_parser_extension_failure(update_path):
    file1 = "png/incorrect_format_1.png"
    file2 = "png/incorrect_format_2.png"
    file1, file2 = update_path(file1, file2)
    with pytest.raises(ValueError) as e:
        gendiff.generate_diff(file1, file2)
    assert str(e.value) == "ERROR: Files have incorrect extension"


@pytest.mark.parametrize(
    "file_path_1, file_path_2",
    [
        ["json/plain1.json", "json/invalid.json"],
        ["yaml/plain1.yml", "yaml/invalid.yml"],
    ],
)
def test_parser_encoder_failure(update_path, file_path_1, file_path_2):
    file_path_1, file_path_2 = update_path(file_path_1, file_path_2)
    with pytest.raises(ValueError) as e:
        gendiff.generate_diff(file_path_1, file_path_2)
    assert str(e.value) == "ERROR: Files contain invalid data"
