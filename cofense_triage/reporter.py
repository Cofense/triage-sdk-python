class Reporter:
    """An end user who has reported a suspicious message"""

    def __init__(self, document):
        self.document = document

    def reporter_id(self):
        return self.document.id

    @property
    def email(self):
        return self.document.email

    @property
    def reports_count(self):
        return self.document.reports_count

    @property
    def last_reported_at(self):
        return self.document.last_reported_at

    @property
    def reputation_score(self):
        return self.document.reputation_score

    @property
    def vip(self):
        return self.document.vip

    @property
    def created_at(self):
        return self.document.created_at

    @property
    def updated_at(self):
        return self.document.updated_at

    @property
    def reports(self):
        from cofense_triage.report import Report

        return (Report(document) for document in self.document.reports)
