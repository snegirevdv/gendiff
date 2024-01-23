import os

import pytest

FIXTURES_PATH = "tests/fixtures/"


@pytest.fixture
def prepare_data():
    def inner(answer_path, file_path_1, file_path_2):
        file_path_1 = get_path(file_path_1)
        file_path_2 = get_path(file_path_2)
        answer_path = get_path(answer_path)

        with open(answer_path) as file:
            answer = file.read()

        return answer, file_path_1, file_path_2

    return inner


@pytest.fixture
def update_path():
    def inner(file_path_1, file_path_2):
        file_path_1 = get_path(file_path_1)
        file_path_2 = get_path(file_path_2)
        return file_path_1, file_path_2

    return inner


def get_path(path):
    return os.path.join(FIXTURES_PATH, path)
