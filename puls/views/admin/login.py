# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Admin, LoginForm
from puls import app

import hashlib
import flask


@app.route("/admin/login/", methods=["GET", "POST"])
@app.template("admin/login.html")
def login():
    form = LoginForm(flask.request.form)
    if flask.request.method == "POST" and form.validate():
        flask.session["user"] = form.user
        return flask.redirect(flask.session.pop("after_login",
                                                flask.url_for("dashboard")))
    return {"form": form}


@app.route("/admin/logout/")
@app.logged_in
def logout():
    del flask.session["user"]
    return flask.redirect(flask.url_for("home"))


@app.route("/admin/bootstrap/")
def bootstrap():
    # check that this is a fresh install (not already bootstrapped)
    if Admin.objects.first():
        return flask.abort(403)

    # build hashed password
    password = "".join([app.config["ACCOUNT_SALT"],
                        app.config["ADMIN_PASSWORD"]]).encode("utf-8")
    password = hashlib.sha512(password).hexdigest()

    # add
    admin = Admin(email=app.config["ADMIN_EMAIL"],
                  password=password,
                  name=app.config["ADMIN_NAME"])
    admin.save()

    # log the newly created user in and redirect to the dashboard
    flask.session["user"] = admin
    return flask.redirect(flask.url_for("dashboard"))
