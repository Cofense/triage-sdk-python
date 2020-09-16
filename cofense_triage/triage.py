from cofense_triage.errors import ReporterNotFoundError
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

    def fetch_reports(self, filter_params=[], resource_type="reports"):
        return (
            Report(document)
            for document in self.api_client.get_document(resource_type, filter_params)
        )

    def fetch_processed_reports(self, filter_params=[]):
        return self.fetch_reports(
            filter_params + [{"attribute": "location", "value": "Processed"}]
        )

    def fetch_processed_reports_since(self, date, filter_params=[]):
        return self.fetch_processed_reports(
            filter_params + [{"attribute": "created_at", "value": date, "op": "gt"}]
        )

    def fetch_processed_reports_by_reporter(self, address, filter_params=[]):
        reporters = list(self.fetch_reporters_by_address(address))

        if not len(reporters) == 1:
            raise ReporterNotFoundError(address)

        return self.fetch_reports(
            filter_params + [{"attribute": "location", "value": "Processed"}],
            resource_type=f"reporters/{reporters[0].reporter_id}/reports",
        )

    def fetch_reporters(self, filter_params=[]):
        return (
            Reporter(document)
            for document in self.api_client.get_document("reporters", filter_params)
        )

    def fetch_reporters_by_address(self, address, filter_params=[]):
        return self.fetch_reporters(
            filter_params + [{"attribute": "email", "value": address}]
        )

    def fetch_threat_indicators(self, attrs):
        pass
