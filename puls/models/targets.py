# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import auto_modified, Searchable, ReferenceField
from puls import app

import mongoengine as mge
import flask_wtf
import datetime
import wtforms as wtf


@auto_modified
class Target(app.db.Document, Searchable):
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


class TargetField(ReferenceField):
    reference_class = Target


class TargetWeightSpec(app.db.EmbeddedDocument):
    target = mge.ReferenceField(Target, required=True)
    value = mge.FloatField(required=True)


class TargetWeightSpecForm(flask_wtf.Form):
    target = TargetField("Target", [wtf.validators.InputRequired()])
    value = wtf.FloatField("Weight", [wtf.validators.InputRequired()])


class TargetWeightField(wtf.FieldList):
    def __init__(self, *args, **kwargs):
        ctor = super(TargetWeightField, self).__init__
        ctor(wtf.FormField(TargetWeightSpecForm),
             *args, **kwargs)

    def process(self, formdata, data=[]):
        targets = set()
        new = []
        try:
            for entry in data:
                if isinstance(entry, TargetWeightSpec):
                    new.append(entry)
                    targets.add(entry.target)
        except TypeError:
            pass

        for target in Target.objects:
            if target not in targets:
                new.append(TargetWeightSpec(target=target, value=0))

        super(TargetWeightField, self).process(formdata, new)

    def populate_obj(self, obj, name):
        if isinstance(obj, (app.db.Document, app.db.EmbeddedDocument)):
            setattr(obj, name, [TargetWeightSpec(**entry.data)
                                for entry in self])
        else:
            super(TargetWeightField, self).populate_obj(obj, name)
