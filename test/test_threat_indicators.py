from cofense_triage.threat_indicators import ThreatIndicators


def test_fetching(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/threat_indicators?per_page=1&page=0",
        text=fixture_from_file("threat_indicators_page0.json"),
    )
    requests_mock.get(
        "https://some-triage-host/api/public/v1/threat_indicators?per_page=1&page=1",
        text=fixture_from_file("threat_indicators_page1.json"),
    )
    requests_mock.get(
        "https://some-triage-host/api/public/v1/threat_indicators?per_page=1&page=2",
        text="[]",
    )

    threat_indicator_pages = ThreatIndicators(triage, {"per_page": 1}).pages

    page1 = next(threat_indicator_pages)
    assert page1[0].threat_value == "malicious.example.com"

    page2 = next(threat_indicator_pages)
    assert page2[0].threat_value == "malicious2.example.com"
