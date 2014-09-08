# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Target, TargetForm
from puls import app

import urllib
import flask


@app.route("/admin/targets/")
@app.template("admin/targets/list.html")
@app.logged_in
def manage_targets():
    return {"items": Target.objects.filter()}


@app.route("/admin/targets/new", methods=["GET", "POST"],
           endpoint="add_target")
@app.route("/admin/targets/<id>/edit", methods=["GET", "POST"])
@app.template("admin/targets/form.html")
@app.logged_in
def edit_target(id=None):
    if id is None:
        item = None
    else:
        try:
            item = Target.objects.get(id=urllib.unquote_plus(id))
        except Target.DoesNotExist:
            return flask.abort(404)

    form = TargetForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Target()
        form.populate_obj(item)
        item.save()
        flask.flash("The target was saved", "success")
        return flask.redirect(flask.url_for("manage_targets"))

    return {"form": form,
            "item": item}


@app.route("/admin/targets/<id>/delete/")
@app.logged_in
def delete_target(id):
    try:
        item = Target.objects.get(id=urllib.unquote_plus(id))

        item.delete()
        flask.flash("Your target has been deleted!", "warning")
        return flask.redirect(flask.url_for("manage_targets"))
    except Target.DoesNotExist:
        return flask.abort(404)
