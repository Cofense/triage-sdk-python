import abc
import json

from cofense_triage.models import RESOURCE_CLASSES_MANY, RESOURCE_CLASSES_SINGLE


class BaseModel(abc.ABC):
    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        if name in RESOURCE_CLASSES_MANY:
            return (
                RESOURCE_CLASSES_MANY[name](resource)
                for resource in self.document[name]
            )
        elif name in RESOURCE_CLASSES_SINGLE:
            return RESOURCE_CLASSES_SINGLE[name](self.document[name])
        else:
            return self.document[name]

    @property
    def resource_id(self):
        return self.document.id

    def to_json(self):
        return json.dumps(self.document.json)
