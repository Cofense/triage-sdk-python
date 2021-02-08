from cofense_triage.models.base_model import BaseModel


RESOURCE_NAME_MANY = "attachment_payloads"
RESOURCE_NAME_SINGLE = "attachment_payload"


class AttachmentPayload(BaseModel):
    """
    Details of a message attachment
    """
