# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Supplier
from puls.compat import unquote_plus
from puls import app

import functools
import flask

@app.route("/suppliers/")
@app.template("suppliers.html")
@app.has_main_menu
def suppliers():
    return {"suppliers": Supplier.objects}


@app.route("/suppliers/<id>/")
@app.template("supplier.html")
@app.has_main_menu
def supplier(id):
    print("HI")
    supplier = Supplier.objects.get_or_404(id=unquote_plus(id))
    return {"supplier": supplier}