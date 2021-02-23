from cofense_triage.models.base_model import BaseModel


RESOURCE_NAME = "reports"


class Report(BaseModel):
    """
    Class representing a Triage report by an end-user of a suspicious message
    """

    @property
    def jpg_url(self):
        return self.document.links.self.url + "/download.jpg"

    @property
    def png_url(self):
        return self.document.links.self.url + "/download.png"
