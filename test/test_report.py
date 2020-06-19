from cofense_triage.report import Report


def test_attrs(requests_mock, triage, fixture_from_file):
    requests_mock.get(
	"https://some-triage-host/api/public/v1/reports/6",
	text=fixture_from_file("single_report.json"),
    )
    requests_mock.get(
        "https://some-triage-host/api/public/v1/reporters/5331",
        text=fixture_from_file("reporters.json"),
    )

    report = Report.fetch(triage, "6")

    assert len(report.attrs) == 25
    assert report.report_id == 13363
    assert report.created_at == "2020-03-19T16:43:09.715Z"
    assert report.reporter.email == "reporter1@example.com"
