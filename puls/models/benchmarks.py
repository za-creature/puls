# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.applications import Application
from puls.models.components import Component
from puls.models.classes import Class
from puls.models import auto_modified

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


class BenchmarkEntry(app.db.EmbeddedDocument):
    component = ReferenceField(Component, required=True)
    score = FloatField(required=True)


@auto_modified
class Benchmark(app.db.Document):  # this is so meta
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    # basic meta
    name = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)

    url = mge.StringField(required=True, max_length=256)
    cls = mge.ReferenceField(Class, required=True)

    factor = mge.FloatField(required=True)  # currently always 0
    exponent = mge.FloatField(required=True)  # currently always 1
    scores = ListField(EmbeddedDocumentField(BenchmarkEntry))

    # dates
    created = DateTimeField(default=datetime.now)
    modified = DateTimeField(default=datetime.now)


class BenchmarkForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])

    factor = wtf.FloatField("Factor", [wtf.validators.Required()])
    exponent = wtf.FloatField("Exponent", [wtf.validators.Required()])
    scores = wtf.FieldList(wtf.FormField(BenchmarkEntryForm), min_entries=1)
