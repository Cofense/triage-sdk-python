import json


def test_parse(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://triage.example.com/api/public/v2/reports",
        text=fixture_from_file("reports.json"),
    )

    report = next(triage.get_reports())

    assert report.resource_id == "1"
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


def test_attachments(requests_mock, triage, fixture_from_file):
    requests_mock.get(
        "https://triage.example.com/api/public/v2/reports",
        text=fixture_from_file("reports.json"),
    )
    requests_mock.get(
        "https://triage.example.com/api/public/v2/reports/1/attachments",
        text=fixture_from_file("attachments.json"),
    )
    requests_mock.get(
        "https://triage.example.com/api/public/v2/attachment_payloads/1",
        text=fixture_from_file("attachment_payloads.json"),
    )

    report = next(triage.get_reports())

    attachment = next(report.attachments)
    assert attachment.filename == "taco_menu.pdf"

    attachment_payload = attachment.attachment_payload
    assert attachment_payload.mime_type == "application/pdf; charset=binary"
