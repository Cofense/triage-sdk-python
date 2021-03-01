import re
import json

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
    requests_mock.post(
        re.compile("https://triage.example.com/"),
        text=fixture_from_file("reports.json"),
    )


def test_get_reporters_by_email(requests_mock, triage):
    list(triage.get_reporters_by_email("reporter1@example.com"))

    assert_get(
        requests_mock.last_request.url,
        "/api/public/v2/reporters",
        {"filter[email]": ["reporter1@example.com"]},
    )


def test_get_resources_no_filter(mocker, triage):
    mocker.patch("cofense_triage.triage_api_client.TriageApiClient.get_documents")

    triage.get_reporters()

    triage.api_client.get_documents.assert_called_with("reporters", [])


def test_get_resources_filter(mocker, triage):
    mocker.patch("cofense_triage.triage_api_client.TriageApiClient.get_documents")

    triage.get_reporters([{"attr": "name", "val": "ggg"}])

    triage.api_client.get_documents.assert_called_with(
        "reporters", [{"attr": "name", "val": "ggg"}]
    )


def test_nonexistant_function(triage):
    with pytest.raises(AttributeError):
        triage.nonexistent_resource_type()


def test_create_resources_list_of_attrs(mocker, triage):
    mocker.patch("cofense_triage.triage_api_client.TriageApiClient.create_documents")

    triage.create_threat_indicators([{"a": 5, "b": 6}, {"a": 7, "b": 8}])

    triage.api_client.create_documents.assert_called_with(
        "threat_indicators", [{"a": 5, "b": 6}, {"a": 7, "b": 8}]
    )


def test_create_resources_kwargs(mocker, triage):
    mocker.patch("cofense_triage.triage_api_client.TriageApiClient.create_documents")

    triage.create_threat_indicators(a=5, b=6)

    triage.api_client.create_documents.assert_called_with(
        "threat_indicators", [{"a": 5, "b": 6}]
    )


def test_create_resources_list_and_kwargs(mocker, triage):
    mocker.patch("cofense_triage.triage_api_client.TriageApiClient.create_documents")

    triage.create_threat_indicators([{"a": 5, "b": 6}], a=7, b=8)

    triage.api_client.create_documents.assert_called_with(
        "threat_indicators", [{"a": 5, "b": 6}, {"a": 7, "b": 8}]
    )


def test_create_threat_indicator(requests_mock, triage):
    triage.create_threat_indicators(
        threat_level="Suspicious", threat_type="Sender", threat_value="evil@example.com"
    )

    # assert requests_mock.call_count == 1
    assert (
        requests_mock.last_request.url
        == "https://triage.example.com/api/public/v2/threat_indicators"
    )
    assert json.loads(requests_mock.last_request.body) == {
        "data": {
            "type": "threat_indicators",
            "attributes": {
                "threat_level": "Suspicious",
                "threat_type": "Sender",
                "threat_value": "evil@example.com",
            },
            "relationships": {},
        }
    }
