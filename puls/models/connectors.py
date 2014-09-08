# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.photos import Photo, PhotoField
from puls.models import auto_modified
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


@auto_modified
class Connector(app.db.Document):
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    name = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)
    photo = mge.ReferenceField(Photo, reverse_delete_rule=mge.NULLIFY)


    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class ConnectorSpec(app.db.EmbeddedDocument):
    connector = mge.ReferenceField(Connector, required=True)
    count = mge.IntField(required=True)


class ConnectorForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])

    photo = PhotoField("Photo", [wtf.validators.InputRequired()])
