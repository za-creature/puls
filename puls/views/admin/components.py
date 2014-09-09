# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Component, ComponentForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/components/", endpoint="manage_components")
@app.route("/admin/components/<int:page>/")
@app.template("admin/components/list.html")
@app.logged_in
def list_components(page=1):
    term = flask.request.form.get("term", "")
    if term:
        page = Component.search(term)
    else:
        page = paginate(Component.objects, page, 20)
    return {"term": term,
            "page": page}


@app.route("/admin/components/search/")
@app.logged_in
def search_components():
    term = flask.request.args.get("term", "")
    if term:
        results = Component.search(term)
    else:
        results = Component.objects.limit(100)

    return flask.jsonify({"results": [{"id": str(item.id),
                                       "text": str(item.name)}
                                      for item in results]})


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
