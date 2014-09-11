# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.compat import str

import mongoengine
import collections
import functools
import importlib
import datetime
import pkgutil
import wtforms as wtf
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


class Searchable(object):
    class NonIterableList(list):
        total = 0

    @classmethod
    def search(self, query, limit=100):
        col = self._get_collection()
        result = col.find({"$text": {"$search": query}},
                          {"score": {"$meta": "textScore"}}) \
                    .sort([("score", {"$meta": "textScore"})]) \
                    .limit(limit)
        return self.NonIterableList([self._from_son(item) for item in result])


class ReferenceField(wtf.HiddenField):
    """Holds a reference to a mongoengine object"""
    @classmethod
    def widget(cls, self, **kwargs):
        if "class_" not in kwargs:
            kwargs["class_"] = ""
        kwargs["class_"] += " combobox"
        return super(ReferenceField, cls).widget(self, **kwargs)

    def process_data(self, value):
        # process initialization data
        if isinstance(value, self.reference_class):
            self.data = value
        else:
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                id = str(valuelist[0])
                self.data = self.reference_class.objects.get(id=id)
            except self.reference_class.DoesNotExist:
                raise wtf.ValidationError("Invalid class id.")
        else:
            self.data = None


class MultiReferenceField(wtf.HiddenField):
    """Holds a reference to zero or more mongoengine objects of the same class
    """
    @classmethod
    def widget(cls, self, **kwargs):
        if "class_" not in kwargs:
            kwargs["class_"] = ""
        kwargs["class_"] += " combobox"
        kwargs["data-multiple"] = True
        kwargs["data-caption"] = ",".join([str(item.name)
                                           for item in self.data])
        if self.data:
            kwargs["value"] = ",".join([str(item.id) for item in self.data])
        return super(MultiReferenceField, cls).widget(self, **kwargs)

    def process_data(self, valuelist):
        # process initialization data
        try:
            self.data = []
            for value in valuelist:
                if isinstance(value, self.reference_class):
                    self.data.append(value)
        except TypeError:
            self.data = None

    def process_formdata(self, valuelist):
        self.data = []
        if valuelist:
            try:
                for id in str(valuelist[0]).split(","):
                    self.data.append(self.reference_class.objects.get(id=id))
            except self.reference_class.DoesNotExist:
                raise wtf.ValidationError("Invalid class id(s).")


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
