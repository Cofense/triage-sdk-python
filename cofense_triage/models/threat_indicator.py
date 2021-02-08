import json


class ThreatIndicator:
    """A threat indicator"""

    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        return self.document[name]

    @property
    def threat_indicator_id(self):
        return self.document.id

    @property
    def reports(self):
        from cofense_triage.report import Report

        return (Report(document) for document in self.document["reports"])

    def to_json(self):
        return json.dumps(self.document.json)


RESOURCE_CLASS = {"threat_indicators": ThreatIndicator}
