import json

from cofense_triage.errors import TriageRequestFailedError
from cofense_triage.report import Report
from cofense_triage.reporter import Reporter
from cofense_triage.threat_indicators import ThreatIndicators
from cofense_triage.triage_api_client import TriageApiClient


class Triage:
    def __init__(self, *, host, api_version, client_id, client_secret):
        self.api_client = TriageApiClient(
            host=host,
            api_version=api_version,
            client_id=client_id,
            client_secret=client_secret,
        )

    def fetch_processed_reports(self):
        self.api_client.get_document("reports")

    def fetch_report(self, report_id):
        return Report.fetch(self, report_id)

    def fetch_reporter(self, reporter_id):
        return Reporter.fetch(self, reporter_id)

    def fetch_threat_indicators(self, attrs):
        return ThreatIndicators(self, attrs)
