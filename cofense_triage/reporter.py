import functools
import json


class Reporter:
    """An end user who has reported a suspicious message"""

    def __init__(self, triage, attrs):
        self.triage = triage
        self.attrs = attrs

    @property
    def email(self):
        return self.attrs["email"]

    @property
    def credibility_score(self):
        return self.attrs["credibility_score"]

    @property
    def reports_count(self):
        return self.attrs["reports_count"]

    @property
    def exists(self):
        return bool(self.attrs)

    def to_json(self):
        return json.dumps(self.attrs)

    @classmethod
    def fetch(cls, triage, reporter_id):
        """Fetch data for the first matching reporter from Triage"""
        response = triage.request(f"reporters/{reporter_id}")

        if not response:
            print(f"could not find report with id {response}")
            return cls(triage, {})

        return cls(triage, response[0])
