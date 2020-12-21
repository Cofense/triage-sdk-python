import json


def test_parse(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://triage.example.com/api/public/v2/reporters",
        text=fixture_from_file("reporters.json"),
    )

    reporter = next(triage.fetch_reporters())

    assert reporter.reporter_id == "1"
    assert reporter.email == "darren@example.com"
    assert reporter.reputation_score == 15
    assert reporter.created_at == "2020-09-22T05:52:20.669Z"

    assert json.loads(reporter.to_json())["attributes"]["email"] == "darren@example.com"
