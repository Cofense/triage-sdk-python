from cofense_triage.models.base_model import BaseModel


RESOURCE_NAME_MANY = "reporters"
RESOURCE_NAME_SINGLE = "reporter"


class Reporter(BaseModel):
    """An end user who has reported a suspicious message"""
