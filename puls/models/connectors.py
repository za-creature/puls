# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.photos import Photo, PhotoField
from puls.models import auto_modified
from puls.compat import str
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


Connectors = Connector._get_collection()


class ConnectorSpec(app.db.EmbeddedDocument):
    connector = mge.ReferenceField(Connector, required=True)
    count = mge.IntField(required=True)


class ConnectorField(wtf.TextField):
    """Holds a reference to a Connector object."""
    def process_data(self, value):
        # process initialization data
        if isinstance(value, Connector):
            self.data = value
        else:
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = Connector.objects.get(id=str(valuelist[0]))
            except Connector.DoesNotExist:
                raise wtf.ValidationError("Invalid connector id.")
        else:
            self.data = None


class ConnectorSpecForm(flask_wtf.Form):
    connector = ConnectorField("Connector")
    count = wtf.IntegerField("Count")


class ConnectorForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])

    photo = PhotoField("Photo", [wtf.validators.InputRequired()])
