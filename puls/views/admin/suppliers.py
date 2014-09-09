# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Supplier, Suppliers, SupplierForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/suppliers/", endpoint="manage_suppliers")
@app.route("/admin/suppliers/<int:page>/")
@app.template("admin/suppliers/list.html")
@app.logged_in
def list_suppliers(page=1):
    return {"page": paginate(Supplier.objects, page, 20)}


@app.route("/admin/manufacturers/search/")
@app.logged_in
def search_suppliers():
    query = flask.request.args.get("term", "")
    return flask.jsonify({"results": [{
        "id": str(item["_id"]),
        "text": str(item["name"])
    }
        for item in Suppliers.find({"$text": {"$search": query}},
                                   {"score": {"$meta": "textScore"}})
                             .sort([("score", {"$meta": "textScore"})])
                             .limit(100)
    ]})


@app.route("/admin/suppliers/new", methods=["GET", "POST"],
           endpoint="add_supplier")
@app.route("/admin/suppliers/<id>/edit", methods=["GET", "POST"])
@app.template("admin/suppliers/form.html")
@app.logged_in
def edit_supplier(id=None):
    if id is None:
        item = None
    else:
        item = Supplier.objects.get_or_404(id=unquote_plus(id))

    form = SupplierForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Supplier()
        form.populate_obj(item)
        item.save()
        flask.flash("The supplier was saved", "success")
        return flask.redirect(flask.url_for("manage_suppliers"))

    return {"form": form,
            "item": item}


@app.route("/admin/suppliers/<id>/delete/")
@app.logged_in
def delete_supplier(id):
    item = Supplier.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your supplier has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_suppliers"))
