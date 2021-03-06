# Cofense Triage SDK for Python

This package provides a object-oriented Python interface to the Triage API V2.
For more information about Cofense Triage, see <https://cofense.com>.

Refer to your Triage API documentation for details about the data schema.

This package works with Triage 1.20 and later.

## Installation

This package is available on PyPI.

```sh
python -m pip install cofense_triage
```

## Usage

### Initialization

First, instantiate a Triage object. `client_id` and `client_secret` values are
provided in the Triage web interface under API V2 Applications. `api_version`
must be `2` for now, and is present to ease future upgrades.

```python
from cofense_triage import Triage

triage = Triage(
    host="https://triage.example.com",
    api_version=2,
    client_id="client_id_here",
    client_secret="client_secret_here",
)
```

### Fetching data

You can fetch resources by calling methods named following the
`get_resourcename()` pattern.

```python
for report in triage.get_reports():
    print(report)

for threat_indicator in triage.get_threat_indicators():
    print(threat_indicator)
```

All `get_*` methods return iterators, which are evaluated lazily—Requests for
subsequent pages of results are made automatically when needed. You can force
all results to be fetched immediately by casting the iterator to a list.

```python
list(triage.get_reporters())
```

The Triage class provides some convenience functions for common requests. See
`cofense_triage/triage.py` for more.

```python
reports = triage.get_processed_reports()

reports = triage.get_processed_reports_since("2020-01-01")

reports = triage.get_processed_reports_by_reporter("j.random@cofense.com")

operators = triage.get_operators_by_email("j.random@cofense.com")
```

You can also pass generic filter conditions into the base `get_*` methods or the
convenience methods. Filter conditions are represented by a dict or list of
dicts, where each dict contains `attr` (attribute name), `val` (value), and
optionally `op` (comparison operation, defaults to `eq`). See the Triage API
documentation for supported attributes and operations, as well as composition
logic.

```python
triage.get_reporters(
    {"attr": "email", "op": "not_end", "val": "example.com"}
)

triage.get_reporters(
    [
        {"attr": "reports_count", "op": "gt", "val": "0"},
        {"attr": "email", "op": "not_end", "val": "example.com"}
    ]
)
```

### Creation

Use methods named following the `create_resourcename()` pattern to create
records. These methods take a single argument, which is a dict or list of dicts
describing the record(s) to be created.

```python
triage.create_rules(
    {
      "name": "Great_New_Rule",
      "priority": 3,
      "scope": "Email",
      "rule_context": "Phishing Tactic",
      "content": "YARA code here",
      "time_to_live": "1 year"
    }
)
```

### Updating

Update records by assigning new values to fields. Call `commit()` to send the
update request to Triage.

```python
rule = next(triage.get_rules({"attr": "name", "val": "Great_New_Rule"}))

rule.priority = 2

rule.commit()
```

### Deletion

Delete records by calling `delete()` followed by `commit()`.

```python
rule = next(triage.get_rules({"attr": "name", "val": "Great_New_Rule"}))

rule.delete()

rule.commit()
```

## Examples

Find all rules with "Credential" in the name and set the priority to 4.

```python
for rule in triage.get_rules({"attr": "name", "val": "Credential", "op": "cont"}):
    rule.priority = 4
    rule.commit()
```

Build a CSV of reporters from the last week, sorted by number of reports.

```python
import datetime
import itertools
import csv

reports = triage.get_reports(
    [
        {
            "attr": "created_at",
            "op": "gt",
            "val": datetime.datetime.now() - datetime.timedelta(days=7),
        }
    ]
)
grouped_reports = itertools.groupby(reports, key=lambda report: report.reporter.email)
results = [
    {
        "address": reporter_address,
        "num_reports": len(list(reports)),
    }
    for reporter_address, reports in grouped_reports
]

with open("reporters_last_week.csv", "w", newline="") as f:
    csv_writer = csv.DictWriter(f, fieldnames=results[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(results)
```

## License

This software is licensed under the MIT License, included in the file `LICENSE`.
