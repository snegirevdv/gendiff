import pytest
import os

FIXTURES_PATH = "tests/fixtures/"


@pytest.fixture
def get_fixture_path():
    def inner(file_path):
        return os.path.join(FIXTURES_PATH, file_path)
    return inner


@pytest.fixture
def get_answer():
    def inner(file_path):
        with open(file_path) as file:
            return file.read()
    return inner
