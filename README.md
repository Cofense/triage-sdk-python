Example usage:

```python
from cofense_triage.triage import Triage

triage = Triage(
    host="https://triage-host-here",
    api_version=2,
    client_id="client_id_here",
    client_secret="client_secret_here",
)

reports = triage.fetch_processed_reports()
print(reports)

reports = triage.fetch_processed_reports_since("2020-07-01")
print(reports)

reports = triage.fetch_processed_reports_by_reporter("j.random@cofense.com")
print(reports)

threat_indicators = triage.fetch_threat_indicators()
print(threat_indicators)

# arbitrary filtering
filter_params = [
    {"attr": "from_address", "op": "cont", "val": "malicious.example.com"},
    {"attr": "reported_at", "op": "gt", "val": "7 days ago"}, # The Triage API accepts any date format that Rails understands
]
reports = triage.fetch_processed_reports(filter_params)
print(reports)
```
