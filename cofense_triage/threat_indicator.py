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
