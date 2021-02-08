from cofense_triage.models.base_model import BaseModel


RESOURCE_NAME_MANY = "attachments"
RESOURCE_NAME_SINGLE = "attachment"


class Attachment(BaseModel):
    """
    Metadata (only) of a message attachment
    """
