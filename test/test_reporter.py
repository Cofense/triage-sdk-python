from cofense_triage.reporter import Reporter


def test_fetch(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/reporters/5",
        text=fixture_from_file("reporters.json"),
    )

    reporter = Reporter.fetch(triage, 5)

    assert reporter.attrs["email"] == "reporter1@example.com"


def test_exists(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://some-triage-host/api/public/v1/reporters/5",
        text=fixture_from_file("reporters.json"),
    )
    requests_mock.get(
        "https://some-triage-host/api/public/v1/reporters/6", text="[]"
    )

    assert Reporter.fetch(triage, 5).exists is True
    assert Reporter.fetch(triage, 6).exists is False
