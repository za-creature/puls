# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from .fields import *

import flask_wtf
import wtforms


class Form(flask_wtf.Form):
    pass