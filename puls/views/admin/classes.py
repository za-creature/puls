# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Class, ClassForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/classes/", endpoint="manage_classes")
@app.route("/admin/classes/<int:page>/")
@app.template("admin/classes/list.html")
@app.logged_in
def list_classes(page=1):
    term = flask.request.form.get("term", "")
    if term:
        page = Class.search(term)
    else:
        page = paginate(Class.objects, page, 20)
    return {"term": term,
            "page": page}


@app.route("/admin/classes/search/")
@app.logged_in
def search_classes():
    term = flask.request.args.get("term", "")
    if term:
        results = Class.search(term)
    else:
        results = Class.objects.limit(100)

    return flask.jsonify({"results": [{"id": str(item.id),
                                       "text": str(item.name)}
                                      for item in results]})


@app.route("/admin/classes/new", methods=["GET", "POST"],
           endpoint="add_class")
@app.route("/admin/classes/<id>/edit", methods=["GET", "POST"])
@app.template("admin/classes/form.html")
@app.logged_in
def edit_class(id=None):
    if id is None:
        item = None
    else:
        item = Class.objects.get_or_404(id=unquote_plus(id))

    form = ClassForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Class()
        form.populate_obj(item)
        item.save()
        flask.flash("The class was saved", "success")
        return flask.redirect(flask.url_for("manage_classes"))

    return {"form": form,
            "item": item}


@app.route("/admin/classes/<id>/delete/")
@app.logged_in
def delete_class(id):
    item = Class.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your class has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_classes"))
