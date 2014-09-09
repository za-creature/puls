# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.manufacturers import Manufacturer, ManufacturerField
from puls.models.connectors import ConnectorSpec, ConnectorSpecForm
from puls.models.suppliers import Supplier, SupplierField
from puls.models.classes import Class, ClassField
from puls.models.photos import Photo, PhotoField
from puls.models import auto_modified
from puls.compat import str
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


@auto_modified
class ExternalComponent(app.db.Document):
    meta = {"indexes": [
        [("supplier", 1), ("name", "text")],
    ]}

    # indexing
    supplier = mge.ReferenceField(Supplier, reverse_delete_rule=mge.CASCADE,
                                  required=True)
    identifier = mge.StringField(required=True, max_length=32,
                                 unique_with="supplier")

    # general data
    name = mge.StringField(required=True, max_length=256)
    price = mge.FloatField(required=True)
    stock = mge.BooleanField()
    url = mge.StringField(required=True, max_length=256)

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


@auto_modified
class Component(app.db.Document):
    name = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)
    photo = mge.ReferenceField(Photo, reverse_delete_rule=mge.NULLIFY)

    classes = mge.ListField(mge.ReferenceField(Class,
                                               reverse_delete_rule=mge.PULL))
    manufacturers = mge.ListField(mge.ReferenceField(Manufacturer,
                                                     reverse_delete_rule=mge.PULL))  # noqa
    connectors = mge.ListField(mge.EmbeddedDocumentField(ConnectorSpec))

    suppliers = mge.ListField(mge.ReferenceField(ExternalComponent))
    metadata = mge.MapField(mge.FloatField())

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


Components = Component._get_collection()


class ComponentField(wtf.TextField):
    """Holds a reference to a Component object. """
    def process_data(self, value):
        # process initialization data
        if isinstance(value, Component):
            self.data = value
        else:
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = Component.objects.get(id=str(valuelist[0]))
            except Component.DoesNotExist:
                raise wtf.ValidationError("Invalid component id.")
        else:
            self.data = None


class ComponentForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.Required(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])
    photo = PhotoField("Photo", [wtf.validators.InputRequired()])

    classes = wtf.FieldList(ClassField("Classes"), min_entries=1)
    manufacturers = wtf.FieldList(ManufacturerField("Manufacturers"),
                                  min_entries=1)
    connectors = wtf.FieldList(wtf.FormField(ConnectorSpecForm),
                               min_entries=1)
    connectors = wtf.FieldList(SupplierField("Suppliers"), min_entries=1)
