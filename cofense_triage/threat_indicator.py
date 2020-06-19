import functools
import json


class ThreatIndicator:
    """A threat indicator"""

    def __init__(self, triage, attrs):
        self.triage = triage
        self.attrs = attrs

    @property
    def report_id(self):
        return self.attrs["report_id"]

    @property
    def threat_key(self):
        return self.attrs["threat_key"]

    @property
    def threat_value(self):
        return self.attrs["threat_value"]

    @property
    def exists(self):
        return bool(self.attrs)

    def to_json(self):
        return json.dumps(self.attrs)

    @classmethod
    def fetch(cls, triage):
        """Fetch threat indicators from Triage"""
        # TODO params.permit(:type, :level, :start_date, :end_date, :page, :per_page)

        response = triage.request(f"threat_indicators")

        return [
            cls(triage, threat_indicator_attrs)
            for threat_indicator_attrs in response
        ]
