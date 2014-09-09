# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Config, Target
from puls import app

import flask


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
