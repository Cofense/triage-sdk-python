import json
import pkg_resources

TRIAGE_SCHEMA = json.load(pkg_resources.resource_stream(__package__, "schema.json"))

from cofense_triage.triage import Triage
