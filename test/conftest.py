import pytest


@pytest.fixture
def fixture_from_file():
    def read_fixture_from_file(fname):
        with open(f"test/fixtures/{fname}", "r") as file:
            return file.read()

    return read_fixture_from_file
