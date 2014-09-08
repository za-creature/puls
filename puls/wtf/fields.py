# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

import wtforms.fields.html5
import wtforms.fields
import flask_wtf.file
import re


__all__ = ["BooleanField", "DateField", "DateTimeField", "DateTimeLocalField",
           "DecimalField", "DecimalRangeField", "EmailField", "FieldList",
           "FileField", "FloatField", "FormField", "HiddenField",
           "IntegerField", "IntegerRangeField", "PasswordField", "RadioField",
           "SearchField", "SelectField", "SelectMultipleField", "SubmitField",
           "StringField", "TelField", "TextField", "TextAreaField", "URLField"]


def timeformat_to_regex(timeformat):
    unsupported = ["%s", "%A", "%b", "%B", "%p", "%Z", "%c", "%x", "%X"]
    translations = {
        "\\%s": "([0-6])",
        "\\%d": "((0[1-9])|([1-2][0-9])|(3[0-1]))",
        "\\%m": "((0[1-9])|(1[0-2]))",
        "\\%y": "([0-9]{2})",
        "\\%Y": "([1-9][0-9]{3})",
        "\\%H": "(([0-1][0-9])|(2[0-3]))",
        "\\%I": "((0[1-9]|1[0-2]))",
        "\\%M": "([0-5][0-9])",
        "\\%S": "([0-5][0-9])",
        "\\%f": "([0-9]{6})",
        "\\%z": "(([\+\-](([0-1][0-9])|(2[0-3]))[0-5][0-9])?)",
        "\\%j": "((00[1-9])|(0[1-9][0-9])|([1-2][0-9][0-9])|(3[0-5][0-9])|(36[0-6]))",  # noqa
        "\\%U": "(([0-4][0-9])|(5[0-3]))",
        "\\%W": "(([0-4][0-9])|(5[0-3]))",
        "\\%\\%": "\\%",
    }

    for pattern in unsupported:
        if pattern in timeformat:
            raise NotImplementedError("{0} is not implemented".format(pattern))

    timeformat = re.escape(timeformat)
    for pattern in translations:
        replacement = translations[pattern]
        timeformat = timeformat.replace(pattern, replacement)
    return "^({0})$".format(timeformat)


class BooleanField(wtforms.fields.BooleanField):
    pass


class DateField(wtforms.fields.html5.DateField):
    pass


class DateTimeField(wtforms.fields.html5.DateTimeField):
    pass


class DateTimeLocalField(wtforms.fields.html5.DateTimeLocalField):
    pass


class DecimalField(wtforms.fields.DecimalField):
    pass


class DecimalRangeField(wtforms.fields.html5.DecimalRangeField):
    pass


class EmailField(wtforms.fields.html5.EmailField):
    pass


class FieldList(wtforms.fields.FieldList):
    pass


class FileField(flask_wtf.file.FileField):
    pass


class FloatField(wtforms.fields.FloatField):
    pass


class FormField(wtforms.fields.FormField):
    pass


class HiddenField(wtforms.fields.HiddenField):
    pass


class IntegerField(wtforms.fields.html5.IntegerField):
    pass


class IntegerRangeField(wtforms.fields.html5.IntegerRangeField):
    pass


class PasswordField(wtforms.fields.PasswordField):
    pass


class RadioField(wtforms.fields.RadioField):
    pass


class SearchField(wtforms.fields.html5.SearchField):
    pass


class SelectField(wtforms.fields.SelectField):
    pass


class SelectMultipleField(wtforms.fields.SelectMultipleField):
    pass


class SubmitField(wtforms.fields.SubmitField):
    pass


class StringField(wtforms.fields.StringField):
    pass


class TelField(wtforms.fields.html5.TelField):
    pass


TextField = StringField


class TextAreaField(wtforms.fields.TextAreaField):
    pass


class URLField(wtforms.fields.html5.URLField):
    pass
