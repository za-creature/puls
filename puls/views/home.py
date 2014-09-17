# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Config, Target, Supplier, Class, Component, System
from puls.tasks import crawl_supplier, generate_top, generate_system
from puls.compat import unquote_plus, str
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
def generate():
    target = Target.objects.get_or_404(id=str(flask.request.form["target"]))
    budget = int(flask.request.form["budget"])
    currency = flask.request.form["currency"]

    rates = Config.get("exchange", {})
    rates["RON"] = 1

    system = generate_system(target, budget / rates[currency])
    if system:
        entry = System(target=target,
                       budget=budget,
                       currency=currency,
                       price=system.price,
                       performance=system.performance,
                       components=system.components)
        entry.save()
        return flask.redirect(flask.url_for("system", id=entry.id))
    else:
        return "FAIL"


@app.route("/system/<id>")
@app.template("system.html")
@app.has_main_menu
def system(id):
    system = System.objects.get_or_404(id=unquote_plus(id))
    rates = Config.get("exchange", {})
    rates["RON"] = 1

    return {"system": system,
            "currency": rates[system.currency]}


@app.route("/about/")
@app.template("about.html")
@app.has_main_menu
def about():
    pass
