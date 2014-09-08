# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Class, ClassForm
from puls import app

import urllib
import flask


@app.route("/admin/classes/")
@app.template("admin/classes/list.html")
@app.logged_in
def manage_classes():
    return {"items": Class.objects.filter()}


@app.route("/admin/classes/new", methods=["GET", "POST"],
           endpoint="add_class")
@app.route("/admin/classes/<id>/edit", methods=["GET", "POST"])
@app.template("admin/classes/form.html")
@app.logged_in
def edit_class(id=None):
    if id is None:
        item = None
    else:
        try:
            item = Class.objects.get(id=urllib.unquote_plus(id))
        except Class.DoesNotExist:
            return flask.abort(404)

    form = ClassForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Class()
        form.populate_obj(item)
        item.save()
        flask.flash("The class was saved", "success")
        return flask.redirect(flask.url_for("manage_classes"))

    return {"form": form,
            "item": item}


@app.route("/admin/classes/<id>/delete/")
@app.logged_in
def delete_class(id):
    try:
        item = Class.objects.get(id=urllib.unquote_plus(id))

        item.delete()
        flask.flash("Your class has been deleted!", "warning")
        return flask.redirect(flask.url_for("manage_classes"))
    except Class.DoesNotExist:
        return flask.abort(404)
