# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Connector, Connectors, ConnectorForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/connectors/", endpoint="manage_connectors")
@app.route("/admin/connectors/<int:page>/")
@app.template("admin/connectors/list.html")
@app.logged_in
def list_connectors(page=1):
    return {"page": paginate(Connector.objects, page, 20)}


@app.route("/admin/connectors/search/")
@app.logged_in
def search_connectors():
    query = flask.request.args.get("term", "")
    return flask.jsonify({"results": [{
        "id": str(item["_id"]),
        "text": str(item["name"])
    }
        for item in Connectors.find({"$text": {"$search": query}},
                                    {"score": {"$meta": "textScore"}})
                              .sort([("score", {"$meta": "textScore"})])
                              .limit(100)
    ]})


@app.route("/admin/connectors/new", methods=["GET", "POST"],
           endpoint="add_connector")
@app.route("/admin/connectors/<id>/edit", methods=["GET", "POST"])
@app.template("admin/connectors/form.html")
@app.logged_in
def edit_connector(id=None):
    if id is None:
        item = None
    else:
        item = Connector.objects.get_or_404(id=unquote_plus(id))

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
    item = Connector.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your connector has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_connectors"))
