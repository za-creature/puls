# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.components import Component
from puls.models.classes import Class, ClassField
from puls.models.targets import Target
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


class System(app.db.Document):
    # basic meta
    target = mge.ReferenceField(Target, required=True)
    budget = mge.FloatField(required=True)
    currency = mge.StringField(required=True)
    price = mge.FloatField(required=True)
    performance = mge.FloatField(required=True)
    components = mge.ListField(mge.ReferenceField(Component))

    created = mge.DateTimeField(default=datetime.datetime.now)
