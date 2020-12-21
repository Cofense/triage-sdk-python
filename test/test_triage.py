import pytest

from cofense_triage import Triage


@pytest.fixture
def triage(mock_oauth_token):
    return Triage(
        host="https://triage.example.com",
        api_version=2,
        client_id="some-client-id",
        client_secret="some-client-secret",
    )


def test_fetch_reporters_by_address(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://triage.example.com/api/public/v2/reporters?filter%5Bemail%5D=reporter1@example.com",
        text=fixture_from_file("reporters_filter_email.json"),
    )

    reporter = next(triage.fetch_reporters_by_address("reporter1@example.com"))

    assert reporter.email == "darren@example.com"
    assert reporter.reputation_score == 15
    assert reporter.created_at == "2020-09-22T05:52:20.669Z"
