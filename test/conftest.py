import pytest

from cofense_triage import Triage


@pytest.fixture
def fixture_from_file():
    def read_fixture_from_file(fname):
        with open(f"test/fixtures/{fname}", "r") as file:
            return file.read()

    return read_fixture_from_file

@pytest.fixture
def triage(mock_oauth_token):
    return Triage(
        host="https://triage.example.com",
        api_version=2,
        client_id="some-client-id",
        client_secret="some-client-secret",
    )

@pytest.fixture
def mock_oauth_token(requests_mock):
    requests_mock.post(
        "https://triage.example.com/oauth/token",
        text="""
            {
                "access_token": "great-access-token",
                "token_type": "bearer",
                "expires_in": 3600,
                "refresh_token": "great-refresh-token"
            }
        """,
    )
