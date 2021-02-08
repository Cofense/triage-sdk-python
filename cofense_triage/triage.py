from cofense_triage.triage_api_client import TriageApiClient
from cofense_triage.errors import ReporterNotFoundError

from cofense_triage.models import RESOURCE_CLASSES


class Triage:
    def __init__(self, *, host, api_version, client_id, client_secret):
        self.api_client = TriageApiClient(
            host=host,
            api_version=api_version,
            client_id=client_id,
            client_secret=client_secret,
        )

    def __getattr__(self, name):
        if name.startswith("create_"):

            def _missing(resources=[], **kwargs):
                # TODO Python 3.9: name = name.removeprefix("create_")
                resource_name = name[7:]

                if isinstance(resources, dict):
                    resources = [resources]
                elif resources is None:
                    resources = []

                if kwargs:
                    resources.append(kwargs)

                return self.api_client.create_documents(resource_name, resources)

            return _missing

    def fetch_reports(self, filter_params=[], resource_type="reports"):
        return (
            RESOURCE_CLASSES["reports"](document)
            for document in self.api_client.get_document(resource_type, filter_params)
        )

    def fetch_processed_reports(self, filter_params=[]):
        return self.fetch_reports(
            filter_params + [{"attr": "location", "val": "Processed"}]
        )

    def fetch_processed_reports_since(self, date, filter_params=[]):
        return self.fetch_processed_reports(
            filter_params + [{"attr": "created_at", "val": date, "op": "gt"}]
        )

    def fetch_processed_reports_by_reporter(self, address, filter_params=[]):
        reporters = list(self.fetch_reporters_by_address(address))

        if not len(reporters) == 1:
            raise ReporterNotFoundError(address)

        return self.fetch_reports(
            filter_params + [{"attr": "location", "val": "Processed"}],
            resource_type=f"reporters/{reporters[0].reporter_id}/reports",
        )

    def fetch_reporters(self, filter_params=[]):
        return (
            RESOURCE_CLASSES["reporters"](document)
            for document in self.api_client.get_document("reporters", filter_params)
        )

    def fetch_attachments(self, filter_params=[]):
        return (
            RESOURCE_CLASSES["attachments"](document)
            for document in self.api_client.get_document("attachments", filter_params)
        )

    def fetch_reporters_by_address(self, address, filter_params=[]):
        return self.fetch_reporters(filter_params + [{"attr": "email", "val": address}])

    def fetch_threat_indicators(self, filter_params=[]):
        return (
            RESOURCE_CLASSES["threat_indicators"](document)
            for document in self.api_client.get_document(
                "threat_indicators", filter_params
            )
        )
