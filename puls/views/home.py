# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Config, Target, Supplier, Class, Component
from puls.tasks import crawl_supplier, generate_top
from puls import app


@app.route("/")
@app.template("home.html")
@app.has_main_menu
def home():
    rates = Config.get("exchange", {})
    rates["RON"] = 1
    return {"rates": rates,
            "targets": Target.objects()}


@app.route("/generate/")
@app.template("home.html")
@app.has_main_menu
def generate():
    pass


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
    cls = Class.objects.get(name="Storage")
    generate_top(cls)

    return "OK"


@app.route("/runtask3")
def runtask3():
    for component in Component.objects:
        component.price = 0
        for external in component.external:
            component.price += external.price
        component.price /= len(component.external)
        component.save()

    return "OK"
