import json


class Report:
    """
    Class representing a Triage report by an end-user of a suspicious message
    """

    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        return self.document[name]

    @property
    def report_id(self):
        return self.document.id

    @property
    def jpg_url(self):
        return self.document.links.self.url + "/download.jpg"

    @property
    def png_url(self):
        return self.document.links.self.url + "/download.png"

    @property
    def reporter(self):
        from cofense_triage.reporter import Reporter

        return Reporter(self.document["reporter"][0])

    def to_json(self):
        return json.dumps(self.document.json)
