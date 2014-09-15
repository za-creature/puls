# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Manufacturer, Target, Component
from puls.compat import unquote_plus
from puls import app, paginate

import functools
import flask

@app.route("/manufacturers/", endpoint="manufacturer_index")
@app.route("/manufacturers/<int:page>/")
@app.template("manufacturers.html")
@app.has_main_menu
def manufacturers(page=1):
    page = paginate(Manufacturer.objects, page, 12)
    return {"page": page}


@app.route("/manufacturers/<id>/")
@app.route("/manufacturers/<id>/<target>/")
@app.route("/manufacturers/<id>/<target>/<sort>/", methods=["GET"],
           endpoint="components_by_manufacturer")
@app.template("manufacturer.html")
@app.has_main_menu
def manufacturer(id, target=None, sort="performance"):
    if target is None:
        target = Target.objects.first()
    else:
        target = Target.objects.get_or_404(id=target)

    if sort != "performance":
        sort = "value"

    manufacturer = Manufacturer.objects.get_or_404(id=unquote_plus(id))
    components = [c for c in Component.objects(__raw__={
        "manufacturers": manufacturer.id,
        "score.target":  target.id
    }).order_by("-score.{0}".format(sort)).limit(100)]

    for component in components:
        for entry in component.score:
            if entry.target == target:
                component.score = getattr(entry, sort)
                break
        else:
            flask.abort(500)

    return {"manufacturer": manufacturer,
            "targets": Target.objects,
            "target": target,
            "sort": sort,
            "components": components,
            "route": functools.partial(flask.url_for,
                                       "components_by_manufacturer",
                                       id=str(manufacturer.id))}
