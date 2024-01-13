from gendiff import generate_diff
import pytest


@pytest.mark.parametrize(
    "answer, file1, file2",
    [
        ["answers/plain.txt", "jsons/plain1.json", "jsons/plain2.json"],
        ["answers/empty.txt", "jsons/empty.json", "jsons/empty.json"],
        ["answers/plain_empty.txt", "jsons/plain1.json", "jsons/empty.json"],
    ]
)
def test_plain(get_answer, get_fixture_path, answer, file1, file2):
    answer_path = get_fixture_path(answer)
    file1 = get_fixture_path(file1)
    file2 = get_fixture_path(file2)

    answer = get_answer(answer_path)

    assert generate_diff(file1, file2) == answer


def test_not_found_error(get_fixture_path):
    file1 = get_fixture_path("jsons/plain1.json")
    file2 = get_fixture_path("jsons/plain2.jsn")
    with pytest.raises(FileNotFoundError):
        generate_diff(file1, file2)


def test_json_error(get_fixture_path):
    file1 = get_fixture_path("jsons/plain1.json")
    file2 = get_fixture_path("jsons/invalid.json")
    with pytest.raises(ValueError):
        generate_diff(file1, file2)
