# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Bus, BusForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/buses/", methods=["GET", "POST"],
           endpoint="manage_buses")
@app.route("/admin/buses/<int:page>/")
@app.template("admin/buses/list.html")
@app.logged_in
def list_buses(page=1):
    term = flask.request.form.get("term", "")
    if term:
        page = Bus.search(term)
    else:
        page = paginate(Bus.objects, page, 20)
    return {"term": term,
            "page": page}


@app.route("/admin/buses/search/")
@app.logged_in
def search_buses():
    term = flask.request.args.get("term", "")
    if term:
        results = Bus.search(term)
    else:
        results = Bus.objects.limit(100)

    return flask.jsonify({"results": [{"id": str(item.id),
                                       "text": str(item.name)}
                                      for item in results]})


@app.route("/admin/buses/new/", methods=["GET", "POST"],
           endpoint="add_bus")
@app.route("/admin/buses/<id>/edit/", methods=["GET", "POST"])
@app.template("admin/buses/form.html")
@app.logged_in
def edit_bus(id=None):
    if id is None:
        item = None
    else:
        item = Bus.objects.get_or_404(id=unquote_plus(id))

    form = BusForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Bus()
        form.populate_obj(item)
        item.save()
        flask.flash("The bus was saved", "success")
        return flask.redirect(flask.url_for("manage_buses"))

    return {"form": form,
            "item": item}


@app.route("/admin/buses/<id>/delete/")
@app.logged_in
def delete_bus(id):
    item = Bus.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your bus has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_buses"))
