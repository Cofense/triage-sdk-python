import importlib
import pkgutil

RESOURCE_CLASSES = {}

for module_info in pkgutil.iter_modules(__path__, prefix=f"{__package__}."):
    module = importlib.import_module(module_info.name)
    if hasattr(module, "RESOURCE_CLASS"):
        RESOURCE_CLASSES |= module.RESOURCE_CLASS
