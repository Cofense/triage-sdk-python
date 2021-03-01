# Cofense Triage SDK for Python

This package provides a object-oriented Python interface to the Triage API V2.
For more information about Cofense Triage, see <https://cofense.com>.

Refer to your Triage API documentation for details about the data schema.

## Installation

This package is available on PyPI.

```sh
python -m pip install cofense_triage
```

## Usage

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

You can fetch resources by calling `get_resourcename()`.

```python
for report in triage.get_reports():
    print(report)

for threat_indicator in triage.get_threat_indicators():
    print(threat_indicators)
```

The Triage class provides some convenience functions for common requests. See
`cofense_triage/triage.py` for more.

```python
reports = triage.get_processed_reports()

reports = triage.get_processed_reports_since("2020-01-01")

reports = triage.get_processed_reports_since("7 days") # The Triage API accepts any date format that Rails understands

reports = triage.get_processed_reports_by_reporter("j.random@cofense.com")

operators = triage.get_operators_by_email("j.random@cofense.com")
```

You can also pass generic filter conditions into the base `get_resourcename()`
methods or the convenience methods. Filter conditions are represented by a list
of dicts, where each dict contains `attr` (attribute name), `val` (value), and
optionally `op` (comparison operation, defaults to `eq`). See the Triage API
documentation for supported attributes and operations.

```python
triage.get_reporters([
    {"attr": "email", "op": "not_end", "val": "example.com"}
])
```
