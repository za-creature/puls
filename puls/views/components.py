# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Class, Target, Component
from puls.compat import unquote_plus
from puls import app

import functools
import flask


@app.route("/components/")
@app.template("components.html")
@app.has_main_menu
def components():
    return {"classes": Class.objects}


@app.route("/classes/<id>/")
@app.route("/classes/<id>/<target>/")
@app.route("/classes/<id>/<target>/<sort>/", methods=["GET"],
           endpoint="components_by_class")
@app.template("class.html")
@app.has_main_menu
def class_(id, target=None, sort="performance"):
    if target is None:
        target = Target.objects.first()
    else:
        target = Target.objects.get_or_404(id=target)

    if sort != "performance":
        sort = "value"

    cls = Class.objects.get_or_404(id=unquote_plus(id))
    components = [c for c in Component.objects(__raw__={
        "score": {
            "$elemMatch": {
                "cls": cls.id,
                "target": target.id
            }
        }
    }).order_by("-score.{0}".format(sort)).limit(100)]

    for component in components:
        for entry in component.score:
            if entry.target == target:
                component.score = getattr(entry, sort)
                break
        else:
            flask.abort(500)

    return {"cls": cls,
            "targets": Target.objects,
            "target": target,
            "sort": sort,
            "components": components,
            "route": functools.partial(flask.url_for, "components_by_class",
                                       id=str(cls.id))}


@app.route("/components/<id>/")
@app.template("component.html")
@app.has_main_menu
def component(id):
    return {"component": Component.objects.get_or_404(id=unquote_plus(id))}
