class Report:
    """
    Class representing a Triage report by an end-user of a suspicious message
    """

    def __init__(self, document):
        self.document = document

    @property
    def report_id(self):
        return self.document.id

    @property
    def location(self):
        return self.document.location

    @property
    def from_address(self):
        return self.document.from_address

    @property
    def subject(self):
        return self.document.subject

    @property
    def received_at(self):
        return self.document.received_at

    @property
    def reported_at(self):
        return self.document.reported_at

    @property
    def headers(self):
        return self.document.headers

    @property
    def body(self):
        return self.document.body

    @property
    def md5(self):
        return self.document.md5

    @property
    def sha256(self):
        return self.document.sha256

    @property
    def match_priority(self):
        return self.document.match_priority

    @property
    def tags(self):
        return self.document.tags

    @property
    def categorization_tags(self):
        return self.document.categorization_tags

    @property
    def processed_at(self):
        return self.document.processed_at

    @property
    def created_at(self):
        return self.document.created_at

    @property
    def updated_at(self):
        return self.document.updated_at

    @property
    def reporter(self):
        from cofense_triage.reporter import Reporter

        return Reporter(self.document.reporter[0])

    def to_json(self):
        return "TODO"  # TODO
