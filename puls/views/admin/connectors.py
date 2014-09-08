# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Connector, ConnectorForm
from puls import app

import urllib
import flask


@app.route("/admin/connectors/")
@app.template("admin/connectors/list.html")
@app.logged_in
def manage_connectors():
    return {"items": Connector.objects.filter()}


@app.route("/admin/connectors/new", methods=["GET", "POST"],
           endpoint="add_connector")
@app.route("/admin/connectors/<id>/edit", methods=["GET", "POST"])
@app.template("admin/connectors/form.html")
@app.logged_in
def edit_connector(id=None):
    if id is None:
        item = None
    else:
        try:
            item = Connector.objects.get(id=urllib.unquote_plus(id))
        except Connector.DoesNotExist:
            return flask.abort(404)

    form = ConnectorForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Connector()
        form.populate_obj(item)
        item.save()
        flask.flash("The connector was saved", "success")
        return flask.redirect(flask.url_for("manage_connectors"))

    return {"form": form,
            "item": item}


@app.route("/admin/connectors/<id>/delete/")
@app.logged_in
def delete_connector(id):
    try:
        item = Connector.objects.get(id=urllib.unquote_plus(id))

        item.delete()
        flask.flash("Your connector has been deleted!", "warning")
        return flask.redirect(flask.url_for("manage_connectors"))
    except Connector.DoesNotExist:
        return flask.abort(404)
