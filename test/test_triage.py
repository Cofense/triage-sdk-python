import re

import pytest


def assert_get(url, expected_path, expected_params):
    import urllib.parse

    parsed_url = urllib.parse.urlparse(url)

    assert parsed_url.path == expected_path
    assert urllib.parse.parse_qs(parsed_url.query) == expected_params


@pytest.fixture(autouse=True)
def mock_all_triage_requests(requests_mock, fixture_from_file):
    requests_mock.get(
        re.compile("https://triage.example.com/"),
        text=fixture_from_file("empty.json"),
    )


def test_fetch_reporters_by_address(requests_mock, triage):
    list(triage.fetch_reporters_by_address("reporter1@example.com"))

    assert_get(
        requests_mock.request_history[-1].url,
        "/api/public/v2/reporters",
        {"filter[email]": ["reporter1@example.com"]},
    )
