# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.manufacturers import Manufacturer
from puls.models.connectors import ConnectorSpec
from puls.models.suppliers import Supplier
from puls.models.classes import Class
from puls.models.photos import Photo
from puls.models import auto_modified
from puls import app

import mongoengine as mge
import datetime


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
    metadata = mge.DictField()

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class ComponentField(flask_wtf.file.FileField):
    """Holds a reference to a Component object. """
