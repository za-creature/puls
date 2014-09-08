"""# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.forms import MultiplePhotoField

from wtforms import *  # noqa


class ComponentForm(Form):
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=4, max=128)])
    description = TextField("Description", [validators.Optional(),
                                            validators.Length(max=4096)])

    photos = MultiplePhotoField("Photos")

    classes = FieldList(StringField("Classes"))
    manufacturers = FieldList(StringField("Manufacturers"))
"""