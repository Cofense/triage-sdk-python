import json


class AttachmentPayload:
    """
    Details of a message attachment
    """

    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        return self.document[name]

    @property
    def attachment_payload_id(self):
        return self.document.id

    @property
    def attachments(self):
        from cofense_triage.attachment import Attachment

        return (Attachment(attachment) for attachment in self.document["attachments"])

    @property
    def reports(self):
        from cofense_triage.report import Report

        return (Report(report) for report in self.document["report"])

    def to_json(self):
        return json.dumps(self.document.json)
