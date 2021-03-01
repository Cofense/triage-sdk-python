from cofense_triage.models.base_model import BaseModel


RESOURCE_NAME = "reporters"


class Reporter(BaseModel):
    """An end user who has reported a suspicious message"""
