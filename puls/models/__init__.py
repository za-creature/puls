# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from flask.ext.mongoengine.wtf import model_form  # noqa

import mongoengine
import collections
import functools
import importlib
import datetime
import pkgutil
import types


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not re-evaluated)."""

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)

        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


def auto_modified(cls):
    def callback(sender, document):
        document.modified = datetime.now()

    mongoengine.signals.pre_save.connect(callback, sender=cls)
    return cls


def has_triggers(cls):
    for name in cls.__dict__:
        fn = getattr(cls, name)
        if isinstance(fn, types.FunctionType) and hasattr(fn, "event"):
            fn.event.connect(lambda sender, document: fn(document),
                             sender=cls)
    return cls


def on(event):
    def wrapper(fn):
        fn.event = event
        return fn
    return wrapper


# import submodule symbols in self
for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module("{0}.{1}".format(__name__, name))
    try:
        symbols = module.__all__
    except AttributeError:
        symbols = filter(lambda name: not name.startswith("_"), dir(module))

    for name in symbols:
        if name not in globals():
            globals()[name] = getattr(module, name)
