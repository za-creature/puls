# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.targets import TargetWeightSpec, TargetWeightField
from puls.models.photos import Photo, PhotoField
from puls.models import (auto_modified, Searchable, ReferenceField,
                         MultiReferenceField)
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


class Metadatum(app.db.EmbeddedDocument):
    name = mge.StringField(required=True, max_length=64)
    unit = mge.StringField(required=True, max_length=16)

    factor = mge.FloatField(default=1)
    exponent = mge.FloatField(default=1)
    weights = mge.ListField(mge.EmbeddedDocumentField(TargetWeightSpec))


@auto_modified
class Class(app.db.Document, Searchable):  # this is so meta
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    name = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)
    photo = mge.ReferenceField(Photo, reverse_delete_rule=mge.NULLIFY)

    metadata = mge.ListField(mge.EmbeddedDocumentField(Metadatum))
    priority = mge.IntField(required=True)
    weights = mge.ListField(mge.EmbeddedDocumentField(TargetWeightSpec))

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class ClassField(ReferenceField):
    reference_class = Class


class MultiClassField(MultiReferenceField):
    reference_class = Class


class MetadatumForm(flask_wtf.Form):
    name = wtf.StringField("Name", [wtf.validators.InputRequired(),
                                    wtf.validators.Length(max=64)])
    unit = wtf.StringField("Unit", [wtf.validators.InputRequired(),
                                    wtf.validators.Length(max=16)])

    factor = wtf.FloatField("Factor", [wtf.validators.InputRequired()])
    exponent = wtf.FloatField("Exponent", [wtf.validators.InputRequired()])
    weights = TargetWeightField()


class ClassForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.InputRequired(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])
    photo = PhotoField("Photo", [wtf.validators.DataRequired()])
    priority = wtf.IntegerField("Priority", [wtf.validators.InputRequired()])
    weights = TargetWeightField("Weights")
