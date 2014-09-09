# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.photos import Photo, PhotoField
from puls.models import auto_modified, Searchable
from puls.compat import str
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
class Class(app.db.Document, Searchable):  # this is so meta
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


class ClassField(wtf.HiddenField):
    """Holds a reference to a Class object."""
    @classmethod
    def widget(cls, self, **kwargs):
        if "class_" not in kwargs:
            kwargs["class_"] = ""
        kwargs["class_"] += " combobox"
        return super(ClassField, self).widget(kwargs)

    def process_data(self, value):
        # process initialization data
        if isinstance(value, Class):
            self.data = value
        else:
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = Class.objects.get(id=str(valuelist[0]))
            except Class.DoesNotExist:
                raise wtf.ValidationError("Invalid class id.")
        else:
            self.data = None


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
    photo = PhotoField("Photo", [wtf.validators.InputRequired()])

    metadata = wtf.FieldList(wtf.FormField(MetadataForm), min_entries=1)
