# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

import importlib
import pkgutil


# import submodule symbols in self
for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module("{0}.{1}".format(__name__, name))
    try:
        symbols = module.__all__
    except AttributeError:
        symbols = [name for name in dir(module) if not name.startswith("_")]

    for name in symbols:
        if name not in globals():
            globals()[name] = getattr(module, name)
