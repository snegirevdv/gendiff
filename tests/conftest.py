import os

import pytest

FIXTURES_PATH = "tests/fixtures/"


@pytest.fixture
def prepare_data():
    def inner(answer_path, file1_path, file2_path):
        file1_path = get_path(file1_path)
        file2_path = get_path(file2_path)
        answer_path = get_path(answer_path)

        with open(answer_path) as file:
            answer = file.read()

        return answer, file1_path, file2_path

    return inner


@pytest.fixture
def update_path():
    def inner(file1_path, file2_path):
        file1_path = get_path(file1_path)
        file2_path = get_path(file2_path)
        return file1_path, file2_path
    return inner


def get_path(path):
    return os.path.join(FIXTURES_PATH, path)
