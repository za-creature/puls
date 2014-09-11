# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Supplier, SupplierForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/suppliers/", methods=["GET", "POST"],
           endpoint="manage_suppliers")
@app.route("/admin/suppliers/<int:page>/")
@app.template("admin/suppliers/list.html")
@app.logged_in
def list_suppliers(page=1):
    term = flask.request.form.get("term", "")
    if term:
        page = Supplier.search(term)
    else:
        page = paginate(Supplier.objects, page, 20)
    return {"term": term,
            "page": page}


@app.route("/admin/manufacturers/search/")
@app.logged_in
def search_suppliers():
    term = flask.request.args.get("term", "")
    if term:
        results = Supplier.search(term)
    else:
        results = Supplier.objects.limit(100)

    return flask.jsonify({"results": [{"id": str(item.id),
                                       "text": str(item.name)}
                                      for item in results]})


@app.route("/admin/suppliers/new/", methods=["GET", "POST"],
           endpoint="add_supplier")
@app.route("/admin/suppliers/<id>/edit/", methods=["GET", "POST"])
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
