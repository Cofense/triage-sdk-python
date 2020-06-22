import itertools

from cofense_triage.threat_indicator import ThreatIndicator


class ThreatIndicators:
    """
    A query and set of matching ThreatIndicator records
    """

    def __init__(self, triage, query):
        self.triage = triage
        self.query = query

    @property
    def pages(self):
        """
        Generates lists of ThreatIndicator objects. One list per page of Triage results.

        Params understood by Triage (TODO version):
            type, level, start_date, end_date, page, per_page
        """

        query_params = self.query

        if "page" not in query_params:
            query_params["page"] = 0

        for _page_offset in itertools.count(1):
            page_response = self.triage.request(
                "threat_indicators", params=query_params,
            )

            yield [ThreatIndicator(self.triage, attrs) for attrs in page_response]

            query_params["page"] = query_params["page"] + 1

            if len(page_response) < (query_params["per_page"] or 10):  # TODO 10 is default? This could be smarter.
                return
