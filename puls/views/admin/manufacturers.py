# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Manufacturer, Manufacturers, ManufacturerForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/manufacturers/", endpoint="manage_manufacturers")
@app.route("/admin/manufacturers/<int:page>/")
@app.template("admin/manufacturers/list.html")
@app.logged_in
def list_manufacturers(page=1):
    return {"page": paginate(Manufacturer.objects, page, 20)}


@app.route("/admin/manufacturers/search/")
@app.logged_in
def search_manufacturers():
    query = flask.request.args.get("term", "")
    return flask.jsonify({"results": [{
        "id": str(item["_id"]),
        "text": str(item["name"])
    }
        for item in Manufacturers.find({"$text": {"$search": query}},
                                       {"score": {"$meta": "textScore"}})
                                 .sort([("score", {"$meta": "textScore"})])
                                 .limit(100)
    ]})


@app.route("/admin/manufacturers/new", methods=["GET", "POST"],
           endpoint="add_manufacturer")
@app.route("/admin/manufacturers/<id>/edit", methods=["GET", "POST"])
@app.template("admin/manufacturers/form.html")
@app.logged_in
def edit_manufacturer(id=None):
    if id is None:
        item = None
    else:
        item = Manufacturer.objects.get_or_404(id=unquote_plus(id))

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
    item = Manufacturer.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your manufacturer has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_manufacturers"))
