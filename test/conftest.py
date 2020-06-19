import pytest

from cofense_triage.triage import Triage


@pytest.fixture
def fixture_from_file():
    def read_fixture_from_file(fname):
        with open(f"test/fixtures/{fname}", "r") as file:
            return file.read()

    return read_fixture_from_file


@pytest.fixture
def triage():
    return Triage(
        host="https://some-triage-host", token="token", user="user", api_version=1
    )
