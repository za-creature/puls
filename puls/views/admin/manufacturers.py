# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Manufacturer, ManufacturerForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/manufacturers/", methods=["GET", "POST"],
           endpoint="manage_manufacturers")
@app.route("/admin/manufacturers/<int:page>/")
@app.template("admin/manufacturers/list.html")
@app.logged_in
def list_manufacturers(page=1):
    term = flask.request.form.get("term", "")
    if term:
        page = Manufacturer.search(term)
    else:
        page = paginate(Manufacturer.objects, page, 20)
    return {"term": term,
            "page": page}


@app.route("/admin/manufacturers/search/")
@app.logged_in
def search_manufacturers():
    term = flask.request.args.get("term", "")
    if term:
        results = Manufacturer.search(term)
    else:
        results = Manufacturer.objects.limit(100)

    return flask.jsonify({"results": [{"id": str(item.id),
                                       "text": str(item.name)}
                                      for item in results]})


@app.route("/admin/manufacturers/new/", methods=["GET", "POST"],
           endpoint="add_manufacturer")
@app.route("/admin/manufacturers/<id>/edit/", methods=["GET", "POST"])
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
