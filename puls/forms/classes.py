"""# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.forms.fields import MultiplePhotoField

from wtforms import *  # noqa


class MetadataForm(Form):
    name = StringField("Name", [validators.Required(),
                                validators.Length(min=2, max=64)])
    unit = StringField("Unit", [validators.Required(),
                                validators.Length(min=1, max=16)])

    comparator = SelectField("Comparator", [validators.Required()],
                             choices=[(0, "Linear"),
                                      (1, "Logarithmic"),
                                      (2, "Exponential")],
                             coerce=int)
    exponent = FloatField("Exponent", [validators.Required()])


class ClassForm(Form):
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=4, max=128)])
    description = TextField("Description", [validators.Optional(),
                                            validators.Length(max=4096)])

    photos = MultiplePhotoField("Photos")

    metadata = FieldList(FormField(MetadataForm))
"""