import importlib
import inspect
import pkgutil

RESOURCE_CLASSES = {}


def build_resource_class(name, document, oauth_session=None):
    return RESOURCE_CLASSES[name](document, oauth_session)


for module_info in pkgutil.iter_modules(__path__, prefix=f"{__package__}."):
    module = importlib.import_module(module_info.name)

    if not hasattr(module, "RESOURCE_NAME"):
        continue

    defined_classes = inspect.getmembers(
        module,
        lambda member: inspect.isclass(member) and member.__module__ == module.__name__,
    )

    # There should only be one (name, class) tuple in the model module. Take the class.
    resource_class = defined_classes[0][1]

    RESOURCE_CLASSES[module.RESOURCE_NAME] = resource_class
