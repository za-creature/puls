# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

import wtforms.validators
import wtforms.widgets
import flask_wtf.file


__all__ = ["AnyOf", "DataRequired", "Email", "EqualTo", "FileAllowed",
           "FileRequired", "IPAddress", "InputRequired", "Length",
           "MacAddress", "NoneOf", "NumberRange", "Optional", "Regexp",
           "Required", "StopValidation", "URL", "UUID", "ValidationError"]


class AnyOf(wtforms.validators.AnyOf):
    def js_args(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext(
                "Invalid value, must be one of: %(values)s." % {
                    "values": self.values_formatter(self.values)})
        return [self.values, message]


class DataRequired(wtforms.validators.DataRequired):
    def js_args(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("This field is required.")

        return [message]


class Email(wtforms.validators.Email):
    pass


class EqualTo(wtforms.validators.EqualTo):
    pass


class FileAllowed(flask_wtf.file.FileAllowed):
    pass


class FileRequired(flask_wtf.file.FileRequired):
    pass


class IPAddress(wtforms.validators.IPAddress):
    pass


class InputRequired(wtforms.validators.InputRequired):
    pass


class Length(wtforms.validators.Length):
    pass


class MacAddress(wtforms.validators.MacAddress):
    pass


class NoneOf(wtforms.validators.NoneOf):
    pass


class NumberRange(wtforms.validators.NumberRange):
    pass


class Optional(wtforms.validators.Optional):
    pass


class Regexp(wtforms.validators.Regexp):
    pass


Required = DataRequired


StopValidation = wtforms.validators.StopValidation


class URL(wtforms.validators.URL):
    pass


class UUID(wtforms.validators.UUID):
    pass


ValidationError = wtforms.validators.ValidationError
