import json


def test_parse(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://triage.example.com/api/public/v2/reports",
        text=fixture_from_file("reports.json"),
    )

    report = next(triage.fetch_reports())

    assert report.report_id == "1"
    assert report.from_address == "zack.bins@example.net"
    assert report.match_priority == 3
    assert report.reported_at == "2020-09-22T05:52:20.859Z"
    assert (
        report.jpg_url
        == "https://triage.example.com/api/public/v2/reports/1/download.jpg"
    )

    assert (
        json.loads(report.to_json())["attributes"]["subject"]
        == "Eveniet voluptatem dolor rerum"
    )
