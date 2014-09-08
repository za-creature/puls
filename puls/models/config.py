# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls import app

import mongoengine as mge
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Config(app.db.Document):
    # authentication information
    key = mge.StringField(required=True, unique=True)
    value = mge.BinaryField(required=True)

    @classmethod
    def get(self, key, default=None):
        entry = self.objects(key=key).first()
        return pickle.loads(entry.value) if entry else default

    @classmethod
    def set(self, key, value):
        entry = self.objects(key=key).first()
        if not entry:
            entry = self(key=key)
        entry.value = pickle.dumps(value)
        entry.save()
