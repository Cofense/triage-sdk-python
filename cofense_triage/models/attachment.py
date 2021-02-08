import json


class Attachment:
    """
    Metadata (only) of a message attachment
    """

    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        return self.document[name]

    @property
    def attachment_id(self):
        return self.document.id

    @property
    def attachment_payload(self):
        from cofense_triage.models.attachment_payload import AttachmentPayload

        return AttachmentPayload(self.document["attachment_payload"])

    @property
    def report(self):
        from cofense_triage.models.report import Report

        return Report(self.document["report"][0])

    def to_json(self):
        return json.dumps(self.document.json)


RESOURCE_CLASS = {"attachments": Attachment}
