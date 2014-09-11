# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.manufacturers import Manufacturer, MultiManufacturerField
from puls.models.buses import Connector
from puls.models.suppliers import Supplier
from puls.models.classes import Class, MultiClassField
from puls.models.photos import Photo, PhotoField
from puls.models import (auto_modified, Searchable, ReferenceField,
                         MultiReferenceField)
from puls.compat import str
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


@auto_modified
class ExternalComponent(app.db.Document, Searchable):
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

    @classmethod
    def search(self, query, supplier, limit=100):
        col = self._get_collection()
        result = col.find({"$text": {"$search": query},
                           "supplier": str(supplier.id)},
                          {"score": {"$meta": "textScore"}}) \
                    .sort([("score", {"$meta": "textScore"})]) \
                    .limit(limit)
        return self.NonIterableList([self._from_son(item) for item in result])


class ExternalComponentField(ReferenceField):
    reference_class = ExternalComponent


class ComponentMetadataSpec(app.db.EmbeddedDocument):
    cls = mge.ReferenceField(Class)
    values = mge.DictField(mge.FloatField)


@auto_modified
class Component(app.db.Document, Searchable):
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    name = mge.StringField(required=True, max_length=256)
    description = mge.StringField(default="", max_length=4096)
    photo = mge.ReferenceField(Photo, reverse_delete_rule=mge.NULLIFY)

    classes = mge.ListField(mge.ReferenceField(Class,
                                               reverse_delete_rule=mge.PULL))
    manufacturers = mge.ListField(mge.ReferenceField(Manufacturer,
                                                     reverse_delete_rule=mge.PULL))  # noqa
    connectors = mge.ListField(mge.EmbeddedDocumentField(Connector))

    external = mge.ListField(mge.ReferenceField(ExternalComponent))
    metadata = mge.ListField(mge.EmbeddedDocumentField(ComponentMetadataSpec))

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class ComponentField(ReferenceField):
    reference_class = Component


class MultiComponentField(MultiReferenceField):
    reference_class = Component


class ComponentForm(flask_wtf.Form):
    name = wtf.TextField("Name", [wtf.validators.InputRequired(),
                                  wtf.validators.Length(max=256)])
    description = wtf.TextAreaField("Description",
                                    [wtf.validators.Length(max=4096)])
    photo = PhotoField("Photo", [wtf.validators.InputRequired()])

    classes = MultiClassField("Classes", [wtf.validators.InputRequired()])
    manufacturers = MultiManufacturerField("Manufacturers",
                                           [wtf.validators.InputRequired()])
    # connectors = wtf.FieldList(wtf.FormField(ConnectorSpecForm))
    # external = wtf.FieldList(ExternalComponentField())
