# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.photos import Photo, PhotoField
from puls.models import auto_modified
from puls import app

import wtforms.fields.html5 as fmm
import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


@auto_modified
class Manufacturer(app.db.Document):
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    name = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)
    photo = mge.ReferenceField(Photo, reverse_delete_rule=mge.NULLIFY)
    url = mge.StringField(required=True, default="")


    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class ManufacturerForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])

    photo = PhotoField("Photo", [wtf.validators.InputRequired()])
    url = fmm.URLField("Website", [wtf.validators.Required(),
                                   wtf.validators.URL()])