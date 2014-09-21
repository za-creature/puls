# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

import wtforms.validators
import wtforms.widgets
import flask_wtf.file
import re


__all__ = ["AnyOf", "DataRequired", "Email", "EqualTo", "FileAllowed",
           "FileRequired", "IPAddress", "InputRequired", "Length",
           "MacAddress", "NoneOf", "NumberRange", "Optional", "Regexp",
           "Required", "StopValidation", "URL", "UUID", "ValidationError"]

StopValidation = wtforms.validators.StopValidation
ValidationError = wtforms.validators.ValidationError


def regex_js_flags(regexp):    
    flags = ""
    for name, value in {"DEBUG": None,
                        "DOTALL": None,
                        "IGNORECASE": "i",
                        "LOCALE": None,
                        "MULTILINE": "m",
                        "TEMPLATE": None,
                        "UNICODE": None,
                        "VERBOSE": None}.items():
        flag = getattr(re, name)
        if regexp.flags & flag:
            if value is None:
                raise NotImplemented("Unsupported regular expression "
                                     "flag: " + name)
            else:
                flags += value
    return flags


class AnyOf(wtforms.validators.AnyOf):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext(
                "Invalid value, must be one of: %(values)s." % {
                    "values": self.values_formatter(self.values)})
        return [self.values, message]


class DataRequired(wtforms.validators.DataRequired):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("This field is required.")
        return [message]


class Email(wtforms.validators.Email):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid email address.")
        return [message]

class EqualTo(wtforms.validators.EqualTo):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("Field must be equal to %(other_name)s.")

        invalid_field_message = field.gettext("Invalid field name '%s'.") % \
                                self.fieldname
        return [self.fieldname, message, invalid_field_message]


class FileAllowed(flask_wtf.file.FileAllowed):
    pass


class FileRequired(flask_wtf.file.FileRequired):
    pass


class IPAddress(wtforms.validators.IPAddress):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid IP address.")
        return [self.ipv4, self.ipv6, message]


class InputRequired(wtforms.validators.InputRequired):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("This field is required.")
        return 


class Length(wtforms.validators.Length):
    def js_args(self, field):
        message = self.message
        if message is None:
            if self.max == -1:
                message = field.ngettext("Field must be at least %(min)d "
                                         "character long.",
                                         "Field must be at least %(min)d "
                                         "characters long.",
                                         self.min)
            elif self.min == -1:
                message = field.ngettext("Field cannot be longer than %(max)d "
                                         "character.",
                                         "Field cannot be longer than %(max)d "
                                         "characters.",
                                         self.max)
            else:
                message = field.gettext("Field must be between %(min)d and "
                                        "%(max)d characters long.")
        return [self.min, self.max, message % {"min": self.min,
                                               "max": self.max})]


class MacAddress(wtforms.validators.MacAddress):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid Mac address.")
        return [message]


class NoneOf(wtforms.validators.NoneOf):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext(
                "Invalid value, can't be any of: %(values)s." % {
                    "values": self.values_formatter(self.values)})
        return [self.values, message]


class NumberRange(wtforms.validators.NumberRange):
    def js_args(self, field):
        message = self.message
        if message is None:
            if self.max is None:
                message = field.gettext("Number must be at least %(min)s.")
            elif self.min is None:
                message = field.gettext("Number must be at most %(max)s.")
            else:
                message = field.gettext("Number must be between %(min)s and "
                                        "%(max)s.")
        return [self.min, self.max, message % {"min": self.min,
                                               "max": self.max})]


class Optional(wtforms.validators.Optional):
    def js_args(self, field):
        return [self.strip_whitespace]


class Regexp(wtforms.validators.Regexp):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid input.")

        return [self.regex.pattern, regex_js_flags(self.regex), message]


Required = InputRequired


class URL(wtforms.validators.URL):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid URL.")
        return [message]


class UUID(wtforms.validators.UUID):
    def js_args(self, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid UUID.")
        return [message]

