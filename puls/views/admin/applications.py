# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls import app


@app.route("/admin/applications/")
@app.template("admin/dashboard.html")
@app.logged_in
def manage_applications():
    pass


"""# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Application
from puls.forms import ApplicationForm
from puls import app

import urllib
import flask


@app.route("/admin/applications")
@app.template("application/list.html")
@app.logged_in
def manage_applications():
    pass


@app.route("/admin/application/", methods=["GET", "POST"],
           endpoint="add_application")
@app.route("/admin/application/<id>/", methods=["GET", "POST"])
@app.template("application/form.html")
@app.logged_in
def edit_application(id=None):
    if id is None:
        item = None
    else:
        try:
            item = Application.objects.get(id=urllib.unquote_plus(id))
        except Application.DoesNotExist:
            return flask.abort(404)

    form = ApplicationForm(flask.request.form, item)

    if flask.request.method == "POST" and form.validate():
        if not item:
            item = Application()

        item.name = form.name.data
        item.description = form.description.data
        item.photos = form.photos.data
        item.url = form.url.data

        item.save()
        flask.flash("The application was saved", "success")
        return flask.redirect(flask.url_for("manage_applications"))

    return {"form": form}


@app.route("/my/albums/<id>/delete/")
@app.logged_in
def delete_application(id):
    try:
        item = Application.objects.get(id=urllib.unquote_plus(id))

        item.delete()
        flask.flash("Your application has been deleted!", "warning")
        return flask.redirect(flask.url_for("manage_applications"))
    except Application.DoesNotExist:
        return flask.abort(404)
"""