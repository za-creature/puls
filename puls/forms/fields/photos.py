"""# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Photo
from puls import config

from bson.objectid import ObjectId
from subprocess import Popen, PIPE
from werkzeug import secure_filename
from wtforms import (Field, HiddenField, FileField, SelectMultipleField,
                     StringField, ValidationError, validators)
from flask import request
from os import stat


class MultiplePhotoField(Field):
    widget = HiddenField()

    def process_formdata(self, valuelist):
        pass"""


