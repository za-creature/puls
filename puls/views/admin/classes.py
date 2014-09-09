# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Class, ClassForm, Metadatum, MetadatumForm
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


@app.route("/admin/classes/new/", methods=["GET", "POST"],
           endpoint="add_class")
@app.route("/admin/classes/<id>/edit/", methods=["GET", "POST"])
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


@app.route("/admin/classes/<id>/meta/")
@app.template("admin/classes/metadata/list.html")
@app.logged_in
def manage_class_meta(id):
    cls = Class.objects.get_or_404(id=unquote_plus(id))
    return {"cls": cls}


@app.route("/admin/classes/<id>/meta/new/", methods=["GET", "POST"],
           endpoint="add_class_meta")
@app.route("/admin/classes/<id>/meta/edit/<name>/", methods=["GET", "POST"])
@app.template("admin/classes/metadata/form.html")
@app.logged_in
def edit_class_meta(id, name=None):
    cls = Class.objects.get_or_404(id=unquote_plus(id))
    if name is None:
        item = None
    else:
        name = unquote_plus(name)
        for index, val in enumerate(cls.metadata):
            if val.name == name:
                item = val
                break
        else:
            flask.abort(404)

    form = MetadatumForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Metadatum()
            cls.metadata.append(item)
            index = -1

        form.populate_obj(cls.metadata[index])
        cls.save()
        flask.flash("The meta entry was saved", "success")
        return flask.redirect(flask.url_for("manage_class_meta",
                                            id=str(cls.id)))

    return {"form": form,
            "item": item,
            "cls": cls}


@app.route("/admin/classes/<id>/metadata/delete/<name>/")
@app.logged_in
def delete_class_meta(id, name):
    cls = Class.objects.get_or_404(id=unquote_plus(id))
    name = unquote_plus(name)
    for index, val in enumerate(cls.metadata):
        if val.name == name:
            break
    else:
        flask.abort(404)

    cls.metadata.pop(index)
    cls.save()
    flask.flash("The meta entry has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_class_meta", id=str(cls.id)))
