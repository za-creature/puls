# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.photos import Photo, PhotoField
from puls.models import auto_modified
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


@auto_modified
class Class(app.db.Document):  # this is so meta
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    name = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)
    photo = mge.ReferenceField(Photo, reverse_delete_rule=mge.NULLIFY)

    metadata = mge.ListField(mge.EmbeddedDocumentField(Metadatum))

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class MetadataForm(flask_wtf.Form):
    name = wtf.StringField("Name", [wtf.validators.Required(),
                                    wtf.validators.Length(max=64)])
    unit = wtf.StringField("Unit", [wtf.validators.Required(),
                                    wtf.validators.Length(max=16)])
    factor = wtf.FloatField("Factor", [wtf.validators.Required()])
    exponent = wtf.FloatField("Exponent", [wtf.validators.Required()])


class ClassForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])

    metadata = wtf.FieldList(wtf.FormField(MetadataForm), min_entries=1)

    photo = PhotoField("Photo", [wtf.validators.InputRequired()])

