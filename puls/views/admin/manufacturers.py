# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Manufacturer, ManufacturerForm
from puls import app

import urllib
import flask


@app.route("/admin/manufacturers/")
@app.template("admin/manufacturers/list.html")
@app.logged_in
def manage_manufacturers():
    return {"items": Manufacturer.objects.filter()}


@app.route("/admin/manufacturers/new", methods=["GET", "POST"],
           endpoint="add_manufacturer")
@app.route("/admin/manufacturers/<id>/edit", methods=["GET", "POST"])
@app.template("admin/manufacturers/form.html")
@app.logged_in
def edit_manufacturer(id=None):
    if id is None:
        item = None
    else:
        try:
            item = Manufacturer.objects.get(id=urllib.unquote_plus(id))
        except Manufacturer.DoesNotExist:
            return flask.abort(404)

    form = ManufacturerForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Manufacturer()
        form.populate_obj(item)
        item.save()
        flask.flash("The manufacturer was saved", "success")
        return flask.redirect(flask.url_for("manage_manufacturers"))

    return {"form": form,
            "item": item}


@app.route("/admin/manufacturers/<id>/delete/")
@app.logged_in
def delete_manufacturer(id):
    try:
        item = Manufacturer.objects.get(id=urllib.unquote_plus(id))

        item.delete()
        flask.flash("Your manufacturer has been deleted!", "warning")
        return flask.redirect(flask.url_for("manage_manufacturers"))
    except Manufacturer.DoesNotExist:
        return flask.abort(404)
