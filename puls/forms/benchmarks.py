"""# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from wtforms import *  # noqa


class BenchmarkForm(Form):
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=4, max=128)])
    description = TextField("Description", [validators.Optional(),
                                            validators.Length(max=4096)])

    cls = TextField("Class", [validators.Required()])
    url = TextField("URL", [validators.Required(),
                            validators.Length(min=4, max=128)])
    cls = TextField("Application", [validators.Required()])

    comparator = SelectField("Comparator", [validators.Required()],
                             choices=[(0, "Linear"),
                                      (1, "Logarithmic"),
                                      (2, "Exponential")],
                             coerce=int)
    exponent = FloatField("Exponent", [validators.Required()])
"""