import pytest

from cofense_triage.errors import TriageRequestFailedError


def test_request(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/processed_reports",
        text=fixture_from_file("processed_reports.json"),
    )

    requests = triage.request("processed_reports")

    assert len(requests) == 2
    assert requests[0]["report_subject"] == "suspicious subject"


def test_request_unsuccessful(requests_mock, triage):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/processed_reports",
        status_code=403,
        text="a bad error",
    )

    with pytest.raises(TriageRequestFailedError) as e:
        triage.request("processed_reports")

        assert e.message == "Call to Cofense Triage failed (403): a bad error"


def test_request_empty(requests_mock, triage):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/processed_reports", text="[]"
    )

    assert triage.request("processed_reports") == {}


def test_request_malformed_json(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/processed_reports",
        text=fixture_from_file("malformed_json.not_json"),
    )

    with pytest.raises(TriageRequestFailedError) as e:
        triage.request("processed_reports")

        assert e.message == "Could not parse result from Cofense Triage (200)"


def test_api_url(triage):
    assert (
        triage.api_url("endpoint")
        == "https://some-triage-host/api/public/v1/endpoint"
    )
    assert (
        triage.api_url("/endpoint")
        == "https://some-triage-host/api/public/v1/endpoint"
    )
    assert (
        triage.api_url("///endpoint/edit?query_string&")
        == "https://some-triage-host/api/public/v1/endpoint/edit?query_string&"
    )
