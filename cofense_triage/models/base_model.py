import abc
import json
from jsonapi_client.relationships import SingleRelationship

from cofense_triage.models import build_resource_class


class BaseModel(abc.ABC):
    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        if name in self.document._relationships.keys_python():
            if isinstance(self.document.relationships[name], SingleRelationship):
                resource_type_name = self.document[name].type
                return build_resource_class(resource_type_name, self.document[name])
            else:
                # it's a to-many relationship, so return a generator
                return (
                    build_resource_class(name, resource)
                    for resource in self.document[name]
                )
        else:
            return self.document[name]

    def __setattr__(self, name, value):
        if name == "document":
            return super().__setattr__(name, value)
        self.document[name] = value

    def delete(self):
        self.document.delete()

    def commit(self):
        self.document.commit()

    @property
    def resource_id(self):
        return self.document.id

    def to_json(self):
        return json.dumps(self.document.json)
