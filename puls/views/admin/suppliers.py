# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Supplier, SupplierForm
from puls import app

import urllib
import flask


@app.route("/admin/suppliers/")
@app.template("admin/suppliers/list.html")
@app.logged_in
def manage_suppliers():
    return {"items": Supplier.objects.filter()}


@app.route("/admin/suppliers/new", methods=["GET", "POST"],
           endpoint="add_supplier")
@app.route("/admin/suppliers/<id>/edit", methods=["GET", "POST"])
@app.template("admin/suppliers/form.html")
@app.logged_in
def edit_supplier(id=None):
    if id is None:
        item = None
    else:
        try:
            item = Supplier.objects.get(id=urllib.unquote_plus(id))
        except Supplier.DoesNotExist:
            return flask.abort(404)

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
    try:
        item = Supplier.objects.get(id=urllib.unquote_plus(id))

        item.delete()
        flask.flash("Your supplier has been deleted!", "warning")
        return flask.redirect(flask.url_for("manage_suppliers"))
    except Supplier.DoesNotExist:
        return flask.abort(404)
