import json


def test_parse(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://triage.example.com/api/public/v2/threat_indicators",
        text=fixture_from_file("threat_indicators.json"),
    )

    threat_indicator = next(triage.fetch_threat_indicators())

    assert threat_indicator.threat_indicator_id == "1"
    assert threat_indicator.threat_type == "Sender"
    assert threat_indicator.threat_value == "zoe.watts@example.org"
    assert threat_indicator.created_at == "2020-09-22T05:52:21.907Z"

    assert (
        json.loads(threat_indicator.to_json())["attributes"]["threat_level"]
        == "Malicious"
    )
