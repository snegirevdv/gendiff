import gendiff
import pytest


@pytest.mark.parametrize(
    "answer, file1, file2",
    [
        ["answers/plain.txt", "json/plain1.json", "json/plain2.json"],
        ["answers/empty.txt", "json/empty.json", "json/empty.json"],
        ["answers/plain_empty.txt", "json/plain1.json", "json/empty.json"],
        ["answers/plain.txt", "yaml/plain1.yml", "yaml/plain2.yml"],
        ["answers/empty.txt", "yaml/empty.yaml", "yaml/empty.yaml"],
        ["answers/plain_empty.txt", "yaml/plain1.yml", "yaml/empty.yaml"],
    ]
)
def test_plain(get_answer, get_fixture_path, answer, file1, file2):
    answer_path = get_fixture_path(answer)
    file1 = get_fixture_path(file1)
    file2 = get_fixture_path(file2)
    answer = get_answer(answer_path)
    assert gendiff.generate_diff(file1, file2) == answer


def test_not_found_error(get_fixture_path):
    file1 = get_fixture_path("json/plain1.json")
    file2 = get_fixture_path("json/plain.json")
    with pytest.raises(FileNotFoundError):
        gendiff.generate_diff(file1, file2)


def test_incorrect_files(get_fixture_path):
    file1 = get_fixture_path("incorrect_format_1.png")
    file2 = get_fixture_path("incorrect_format_2.png")
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
def test_encoder_error(get_fixture_path, file1, file2):
    file1 = get_fixture_path(file1)
    file2 = get_fixture_path(file2)
    with pytest.raises(ValueError) as e:
        gendiff.generate_diff(file1, file2)
    assert str(e.value) == "ERROR: Files contain invalid data"
