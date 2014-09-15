# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Config, Target, Supplier, Class, Component, System
from puls.tasks import (crawl_supplier, generate_top, generate_system,
                        update_exchange)
from puls import app

import datetime
import flask


@app.route("/admin/tasks/crawl/<id>")
def crawl(id):
    crawl_supplier(Supplier.objects.get_or_404(id=unquote_plus(id)))
    return "OK"


@app.route("/admin/tasks/exchange/")
def get_exchange():
    update_exchange()
    return "OK"


@app.route("/admin/tasks/top/")
def build_top():
    result = ""
    for cls in Class.objects:
        result += cls.name + " "
        try:
            generate_top(cls)
            result += "OK"
        except Exception:
            import traceback
            result += "FAIL"
        result += "<br/>"
    return result


@app.route("/admin/tasks/prices/")
def get_prices():
    for component in Component.objects:
        component.price = 0
        for external in component.external:
            component.price += external.price
        component.price /= len(component.external)
        component.save()
    return "OK"
