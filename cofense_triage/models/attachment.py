from cofense_triage.models.base_model import BaseModel


RESOURCE_NAME = "attachments"


class Attachment(BaseModel):
    """
    Metadata (only) of a message attachment
    """
