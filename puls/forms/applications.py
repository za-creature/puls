"""# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.forms.fields import MultiplePhotoField

from wtforms import *  # noqa


class ApplicationForm(Form):
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=4, max=128)])
    description = TextField("Description", [validators.Optional(),
                                            validators.Length(max=4096)])

    photos = MultiplePhotoField("Photos")

    url = TextField("URL", [validators.Required(),
                            validators.Length(min=4, max=128)])
"""