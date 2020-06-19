import functools
import json


class Report:
    """
    Class representing a Triage report by an end-user of a suspicious message
    """

    def __init__(self, triage, attrs):
        self.triage = triage
        self.attrs = attrs

    @property
    def report_id(self):
        return self.attrs["id"]

    @property
    def report_body(self):
        return self.attrs["report_body"]

    @property
    def created_at(self):
        return self.attrs["created_at"]

    @property
    def reporter_id(self):
        return self.attrs["reporter_id"]

    @property
    @functools.lru_cache()
    def reporter(self):
        return self.triage.fetch_reporter(self.attrs["reporter_id"])

    @property
    def exists(self):
        return bool(self.attrs)

    def to_json(self):
        return json.dumps(self.attrs)

    @classmethod
    def fetch(cls, triage, report_id):
        """Fetch data for the first matching report from Triage"""

        response = triage.request(f"reports/{report_id}")

        if not response:
            print(f"could not find report with id {response}")
            return cls(triage, {})

        return cls(triage, response[0])
