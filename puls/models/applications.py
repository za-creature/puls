"""# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models.photos import Photo
from puls.models import auto_modified

from mongoengine import *  # noqa
from datetime import datetime


@auto_modified
class Application(Document):
    meta = {"indexes": [
        [("name", "text"), ("description", "text")],
    ]}

    name = StringField(required=True, max_length=256)
    description = StringField(default="", max_length=4096)
    photos = ListField(ReferenceField(Photo, reverse_delete_rule=PULL))
    url = StringField(required=True, default="")

    # dates
    created = DateTimeField(default=datetime.now)
    modified = DateTimeField(default=datetime.now)
"""