# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import auto_modified
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


@auto_modified
class Target(app.db.Document):
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    name = mge.StringField(required=True, max_length=256, unique=True)
    icon = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class TargetForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    icon = wtf.TextField("Glyphicon", [wtf.validators.Required(),
                                       wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])
