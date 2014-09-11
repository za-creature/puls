# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.components import Component, ComponentField
from puls.models.classes import Class, ClassField
from puls.models import auto_modified, Searchable
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


class BenchmarkEntry(app.db.EmbeddedDocument):
    component = mge.ReferenceField(Component, required=True)
    score = mge.FloatField(required=True)


@auto_modified
class Benchmark(app.db.Document, Searchable):
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
    entries = mge.ListField(mge.EmbeddedDocumentField(BenchmarkEntry))

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class BenchmarkEntryForm(flask_wtf.Form):
    component = ComponentField("Component", [wtf.validators.InputRequired()])
    score = wtf.FloatField("Score", [wtf.validators.InputRequired()])


class BenchmarkForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])

    url = wtf.TextField("URL", [wtf.validators.InputRequired(),
                                wtf.validators.Length(max=256)])
    cls = ClassField("Component Class", [wtf.validators.InputRequired()])


    factor = wtf.FloatField("Factor", [wtf.validators.InputRequired()])
    exponent = wtf.FloatField("Exponent", [wtf.validators.InputRequired()])

