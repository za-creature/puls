# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import memoized
from puls import app

import mongoengine as mge
import datetime
import wtforms as wtf
import flask_wtf
import hashlib


class Admin(app.db.Document):
    # authentication information
    email = mge.EmailField(required=True, unique=True, min_length=6,
                           max_length=64)
    password = mge.StringField(required=True)

    # profile info
    name = mge.StringField(required=True, max_length=128)

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)
    modified = mge.DateTimeField(default=datetime.datetime.now)


class LoginForm(flask_wtf.Form):
    """Validates an e-mail address and provides a 'user' property that
    references the user bound to said e-mail address."""
    email = wtf.TextField("E-mail address", [wtf.validators.Required(),
                                             wtf.validators.Length(min=4,
                                                                   max=64),
                                             wtf.validators.Email()])
    password = wtf.PasswordField("Password", [wtf.validators.Required(),
                                              wtf.validators.Length(min=4,
                                                                    max=64)])

    @property
    @memoized
    def user(form):
        return Admin.objects(email=form.email.data).first()

    def validate_email(form, field):
        if form.user is None:
            raise wtf.ValidationError("User does not exist")

    def validate_password(form, field):
        password = "".join([app.config["ACCOUNT_SALT"],
                            field.data]).encode("utf-8")
        password = hashlib.sha512(password).hexdigest()

        if form.user and form.user.password != password:
            raise wtf.ValidationError("Invalid password")
