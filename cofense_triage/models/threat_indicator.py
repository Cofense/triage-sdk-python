from cofense_triage.models.base_model import BaseModel


RESOURCE_NAME_MANY = "threat_indicators"
RESOURCE_NAME_SINGLE = "threat_indicator"


class ThreatIndicator(BaseModel):
    """A threat indicator"""
