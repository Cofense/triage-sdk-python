import abc
import json
from jsonapi_client.relationships import SingleRelationship

from cofense_triage.models import RESOURCE_CLASSES


class BaseModel(abc.ABC):
    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        if name in self.document._relationships.keys_python():
            if isinstance(self.document.relationships[name], SingleRelationship):
                resource_type_name = self.document[name].type
                return RESOURCE_CLASSES[resource_type_name](self.document[name])
            else:
                # it's a to-many relationship, so return a generator
                return (
                    RESOURCE_CLASSES[name](resource) for resource in self.document[name]
                )
        else:
            return self.document[name]

    @property
    def resource_id(self):
        return self.document.id

    def to_json(self):
        return json.dumps(self.document.json)
