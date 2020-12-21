import json


class Reporter:
    """An end user who has reported a suspicious message"""

    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        return self.document[name]

    @property
    def reporter_id(self):
        return self.document.id

    @property
    def reports(self):
        from cofense_triage.report import Report

        return (Report(document) for document in self.document["reports"])

    def to_json(self):
        return json.dumps(self.document.json)
