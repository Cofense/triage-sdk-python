import re

import pytest


@pytest.fixture(autouse=True)
def mock_all_triage_requests(requests_mock, fixture_from_file):
    requests_mock.get(
        re.compile("https://triage.example.com/"),
        text=fixture_from_file("empty.json"),
    )


def test_fetch_reporters_by_address(requests_mock, triage):
    list(triage.fetch_reporters_by_address("reporter1@example.com"))

    assert requests_mock.request_history[-1].url.endswith(
        "/reporters?filter%5Bemail%5D=reporter1@example.com"
    )
