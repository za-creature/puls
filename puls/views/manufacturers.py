# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Manufacturer
from puls.compat import unquote_plus
from puls import app

import functools
import flask

@app.route("/manufacturers/")
@app.template("manufacturers.html")
@app.has_main_menu
def manufacturers():
    return {"manufacturers": Manufacturer.objects}


@app.route("/suppliers/<id>/")
@app.template("manufacturer.html")
@app.has_main_menu
def manufacturer(id):
    manufacturer = Manufacturer.objects.get_or_404(id=unquote_plus(id))
    return {"manufacturer": manufacturer}