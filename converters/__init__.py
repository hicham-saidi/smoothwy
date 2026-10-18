"""
Converter registry.

Every module in this folder that defines a BaseConverter subclass is picked up
automatically. To add a new file type: drop a new file here, subclass
BaseConverter, done. No other file needs to change.
"""
from __future__ import annotations

import importlib
import inspect
import pkgutil

from .base import BaseConverter, ConversionOptions

__all__ = ["BaseConverter", "ConversionOptions", "get_converters"]


def get_converters() -> dict[str, BaseConverter]:
    found: dict[str, BaseConverter] = {}
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name == "base":
            continue
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, BaseConverter) and cls is not BaseConverter and cls.name:
                found[cls.name] = cls()
    return dict(sorted(found.items()))
