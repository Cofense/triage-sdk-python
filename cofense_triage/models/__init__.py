import importlib
import inspect
import pkgutil

RESOURCE_CLASSES_MANY = {}
RESOURCE_CLASSES_SINGLE = {}

for module_info in pkgutil.iter_modules(__path__, prefix=f"{__package__}."):
    module = importlib.import_module(module_info.name)

    if not hasattr(module, "RESOURCE_NAME_MANY"):
        continue

    defined_classes = inspect.getmembers(
        module,
        lambda member: inspect.isclass(member) and member.__module__ == module.__name__,
    )

    # There should only be one (name, class) tuple in the model module. Take the class.
    resource_class = defined_classes[0][1]

    RESOURCE_CLASSES_MANY[module.RESOURCE_NAME_MANY] = resource_class
    RESOURCE_CLASSES_SINGLE[module.RESOURCE_NAME_SINGLE] = resource_class
