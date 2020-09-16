class ThreatIndicator:
    """A threat indicator"""

    def __init__(self, document):
        self.document = document

    @property
    def threat_indicator_id(self):
        return self.document.id

    @property
    def threat_level(self):
        return self.document["threat_level"]

    @property
    def threat_type(self):
        return self.document["threat_type"]

    @property
    def threat_value(self):
        return self.document["threat_value"]

    @property
    def created_at(self):
        return self.document["created_at"]

    @property
    def updated_at(self):
        return self.document["updated_at"]

    @property
    def reports(self):
        from cofense_triage.report import Report

        return (Report(document) for document in self.document["reports"])
