# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Connector, ConnectorForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/connectors/", endpoint="manage_connectors")
@app.route("/admin/connectors/<int:page>/")
@app.template("admin/connectors/list.html")
@app.logged_in
def list_connectors(page=1):
    term = flask.request.form.get("term", "")
    if term:
        page = Connector.search(term)
    else:
        page = paginate(Connector.objects, page, 20)
    return {"term": term,
            "page": page}


@app.route("/admin/connectors/search/")
@app.logged_in
def search_connectors():
    term = flask.request.args.get("term", "")
    if term:
        results = Connector.search(term)
    else:
        results = Connector.objects.limit(100)

    return flask.jsonify({"results": [{"id": str(item.id),
                                       "text": str(item.name)}
                                      for item in results]})


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
