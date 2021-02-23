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
        if name.startswith("get_"):
            # TODO Python 3.9: name = name.removeprefix("create_")
            resource_name = name[4:]
            return self._get_resources_function(resource_name)
        elif name.startswith("create_"):
            # TODO Python 3.9: name = name.removeprefix("create_")
            resource_name = name[7:]
            return self._create_resources_function(resource_name)
        else:
            raise AttributeError(name)

    def _create_resources_function(self, resource_name):
        def _function(resources=[], **kwargs):
            if isinstance(resources, dict):
                resources = [resources]
            elif resources is None:
                resources = []

            if kwargs:
                resources.append(kwargs)

            return self.api_client.create_documents(resource_name, resources)

        return _function

    def _get_resources_function(self, resource_name):
        resource_class = RESOURCE_CLASSES[resource_name]

        def _function(filter_params=[]):
            return (
                resource_class(document)
                for document in self.api_client.get_documents(
                    resource_name, filter_params
                )
            )

        return _function

    def get_processed_reports(self, filter_params=[]):
        return self.get_reports(
            filter_params + [{"attr": "location", "val": "Processed"}]
        )

    def get_processed_reports_since(self, date, filter_params=[]):
        return self.get_processed_reports(
            filter_params + [{"attr": "created_at", "val": date, "op": "gt"}]
        )

    def get_processed_reports_by_reporter(self, address, filter_params=[]):
        reporters = list(self.get_reporters_by_address(address))

        if not len(reporters) == 1:
            raise ReporterNotFoundError(address)

        return self.get_reports(
            filter_params + [{"attr": "location", "val": "Processed"}],
            resource_type=f"reporters/{reporters[0].resource_id}/reports",
        )

    def get_reporters_by_email(self, address, filter_params=[]):
        # TODO handle list of addresses
        return self.get_reporters(filter_params + [{"attr": "email", "val": address}])
