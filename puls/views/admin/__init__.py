# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

import importlib
import pkgutil


# import all submodules
for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    importlib.import_module("{0}.{1}".format(__name__, name))
