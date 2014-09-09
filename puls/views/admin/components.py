# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Component, Components, ComponentForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/components/", endpoint="manage_components")
@app.route("/admin/components/<int:page>/")
@app.template("admin/components/list.html")
@app.logged_in
def list_components(page=1):
    return {"page": paginate(Component.objects, page, 20)}


@app.route("/admin/components/search/")
@app.logged_in
def search_components():
    query = flask.request.args.get("term", "")
    return flask.jsonify({"results": [{
        "id": str(item["_id"]),
        "text": str(item["name"])
    }
        for item in Components.find({"$text": {"$search": query}},
                                    {"score": {"$meta": "textScore"}})
                              .sort([("score", {"$meta": "textScore"})])
                              .limit(100)
    ]})


@app.route("/admin/components/new", methods=["GET", "POST"],
           endpoint="add_component")
@app.route("/admin/components/<id>/edit", methods=["GET", "POST"])
@app.template("admin/components/form.html")
@app.logged_in
def edit_component(id=None):
    if id is None:
        item = None
    else:
        item = Component.objects.get_or_404(id=unquote_plus(id))

    form = ComponentForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Component()
        form.populate_obj(item)
        item.save()
        flask.flash("The component was saved", "success")
        return flask.redirect(flask.url_for("manage_components"))

    return {"form": form,
            "item": item}


@app.route("/admin/components/<id>/delete/")
@app.logged_in
def delete_component(id):
    item = Component.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your component has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_components"))
