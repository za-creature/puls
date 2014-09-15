# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Supplier
from puls.compat import unquote_plus
from puls import app, paginate

import functools
import flask

@app.route("/suppliers/", endpoint="supplier_index")
@app.route("/suppliers/<int:page>/")
@app.template("suppliers.html")
@app.has_main_menu
def suppliers(page=1):
    page = paginate(Supplier.objects, page, 12)
    return {"page": page}


@app.route("/suppliers/<id>/")
@app.template("supplier.html")
@app.has_main_menu
def supplier(id):
    supplier = Supplier.objects.get_or_404(id=unquote_plus(id))
    return {"supplier": supplier}