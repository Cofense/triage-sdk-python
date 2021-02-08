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
    def attachments(self):
        from cofense_triage.models.attachment import Attachment

        return (Attachment(attachment) for attachment in self.document["attachments"])

    @property
    def reporter(self):
        from cofense_triage.models.reporter import Reporter

        return Reporter(self.document["reporter"][0])

    def to_json(self):
        return json.dumps(self.document.json)


RESOURCE_CLASS = {"reports": Report}
