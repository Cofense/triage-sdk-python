import json
import requests

from cofense_triage.errors import TriageRequestFailedError
from cofense_triage.report import Report
from cofense_triage.reporter import Reporter
from cofense_triage.threat_indicator import ThreatIndicator


class Triage:
    def __init__(self, *, host, token, user, api_version):
        self.host = host
        self.token = token
        self.user = user
        self.api_version = api_version

    def request(self, endpoint, params=None, body=None):
        """
        Make a request to the configured Triage instance and return the result.
        """
        response = requests.get(
            self.api_url(endpoint),
            headers={
                "Authorization": f"Token token={self.user}:{self.token}",
                "Accept": "application/json",
            },
            params=params,
            data=body,
        )

        if not response.ok:
            raise TriageRequestFailedError(response.status_code, response.text)

        if response.status_code == 206:
            # 206 indicates Partial Content. The reason will be in the warning header.
            print(str(response.headers))

        if not response.text or response.text == "[]":
            return {}

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise TriageRequestFailedError(
                response.status_code, "Could not parse result from Triage"
            )

    def fetch_report(self, report_id):
        return Report.fetch(self, report_id)

    def fetch_reporter(self, reporter_id):
        return Reporter.fetch(self, reporter_id)

    def fetch_threat_indicators(self):
        return ThreatIndicator.fetch(self)

    def api_url(self, endpoint):
        """Return a full URL for the configured Triage host and the specified endpoint"""
        endpoint = endpoint.lstrip("/")

        if self.api_version == 1:
            return f"{self.host}/api/public/v1/{endpoint}"
        else:
            raise "unsupported API version"
