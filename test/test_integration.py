import pytest


@pytest.fixture(autouse=True)
def mock_triage_responses(requests_mock, fixture_from_file):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/reporters/5331",
        text=fixture_from_file("reporters.json"),
    )
    requests_mock.get(
        "https://some-triage-host/api/public/v1/reports/13363",
        text=fixture_from_file("single_report.json"),
    )
    requests_mock.get(
        "https://some-triage-host/api/public/v1/threat_indicators",
        text=fixture_from_file("threat_indicators.json"),
    )


def test_fetch_reporter(triage):
    reporter = triage.fetch_reporter(5331)

    assert reporter.email == "reporter1@example.com"


def test_fetch_report(triage):
    report = triage.fetch_report(13363)

    assert report.report_body[:15] == "From: Sender <s"
    assert report.reporter.email == "reporter1@example.com"


def test_fetch_threat_indicators(triage):
    threat_indicators = triage.fetch_threat_indicators()

    assert threat_indicators[0].threat_key == "Domain"
    assert threat_indicators[0].threat_value == "malicious.example.com"
