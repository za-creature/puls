# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Config, Target, Supplier, Class, Component
from puls.tasks import crawl_supplier, generate_top, generate_system
from puls import app

import datetime
import flask


@app.route("/")
@app.template("home.html")
@app.has_main_menu
def home():
    rates = Config.get("exchange", {})
    rates["RON"] = 1
    return {"rates": rates,
            "targets": Target.objects()}


@app.route("/generate/", methods=["GET", "POST"])
@app.template("system.html")
@app.has_main_menu
def generate():
    target = Target.objects.get_or_404(id=str(flask.request.form["target"]))
    budget = int(flask.request.form["budget"])
    return {"target": target,
            "budget": budget,
            "timestamp": datetime.datetime.now(),
            "system": generate_system(target, budget)}


@app.route("/about/")
@app.template("about.html")
@app.has_main_menu
def about():
    pass


@app.route("/runtask")
def runtask():
    pcgarage = Supplier.objects.get_or_404(name="eMag")
    crawl_supplier(pcgarage)

    return "OK"


@app.route("/runtask2")
def runtask2():
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


@app.route("/runtask3")
def runtask3():
    for component in Component.objects:
        component.price = 0
        for external in component.external:
            component.price += external.price
        component.price /= len(component.external)
        component.save()

    return "OK"
