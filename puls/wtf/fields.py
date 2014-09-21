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
    def js_args(self):
        return [self.false_values]


class DateField(wtforms.fields.html5.DateField):
    def js_args(self):
        return [self.format, self.gettext("Not a valid date.")]


class DateTimeField(wtforms.fields.html5.DateTimeField):
    def js_args(self):
        return [self.format, self.gettext("Not a valid date and / or time.")]


class DateTimeLocalField(wtforms.fields.html5.DateTimeLocalField):
    def js_args(self):
        return [self.format, self.gettext("Not a valid date and / or time.")]


class DecimalField(wtforms.fields.DecimalField):
    def js_args(self):
        return self.gettext("Not a valid decimal value.")


class DecimalRangeField(wtforms.fields.html5.DecimalRangeField):
    def js_args(self):
        return self.gettext("Not a valid decimal range.")


class EmailField(wtforms.fields.html5.EmailField):
    def js_args(self):
        return []


class FieldList(wtforms.fields.FieldList):
    pass


class FileField(flask_wtf.file.FileField):
    pass


class FloatField(wtforms.fields.FloatField):
    def js_args(self):
        return self.gettext("Not a valid float value.")


class FormField(wtforms.fields.FormField):
    pass


class HiddenField(wtforms.fields.HiddenField):
    def js_args(self):
        return []


class IntegerField(wtforms.fields.html5.IntegerField):
    def js_args(self):
        return self.gettext("Not a valid integer value.")


class IntegerRangeField(wtforms.fields.html5.IntegerRangeField):
    def js_args(self):
        return self.gettext("Not a valid integer range.")


class PasswordField(wtforms.fields.PasswordField):
    def js_args(self):
        return []


class RadioField(wtforms.fields.RadioField):
    pass


class SearchField(wtforms.fields.html5.SearchField):
    def js_args(self):
        return []


class SelectField(wtforms.fields.SelectField):
    def js_args(self):
        if self.coerce is int:
            coerce_mode = "int"
        elif self.coerce is float:
            coerce_mode = "float"
        else:
            coerce_mode = "str"
        return [coerce_mode, self.gettext("Invalid Choice: could not coerce.")]


class SelectMultipleField(wtforms.fields.SelectMultipleField):
    def js_args(self):
        if self.coerce is int:
            coerce_mode = "int"
        elif self.coerce is float:
            coerce_mode = "float"
        else:
            coerce_mode = "str"
        return [coerce_mode, self.gettext("Invalid choice(s): one or more "
                                          "values could not be coerced.")]

class SubmitField(wtforms.fields.SubmitField):
    def js_args(self):
        return []


class StringField(wtforms.fields.StringField):
    def js_args(self):
        return []


class TelField(wtforms.fields.html5.TelField):
    def js_args(self):
        return []


TextField = StringField


class TextAreaField(wtforms.fields.TextAreaField):
    def js_args(self):
        return []


class URLField(wtforms.fields.html5.URLField):
    def js_args(self):
        return []
