# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Component, ComponentForm, ComponentMetadataSpec
from puls.compat import unquote_plus, str
from puls import app, paginate

import flask_wtf
import wtforms as wtf
import hashlib
import flask


@app.route("/admin/components/", methods=["GET", "POST"],
           endpoint="manage_components")
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


@app.route("/admin/components/new/", methods=["GET", "POST"],
           endpoint="add_component")
@app.route("/admin/components/<id>/edit/", methods=["GET", "POST"])
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
        flask.flash("The component was saved. Please update the metadata "
                    "if new classes were added", "success")
        return flask.redirect(flask.url_for("edit_component_meta",
                                            id=str(item.id)))

    return {"form": form,
            "item": item}


@app.route("/admin/components/<id>/metadata/", methods=["GET", "POST"])
@app.template("admin/components/metadata.html")
@app.logged_in
def edit_component_meta(id=None):
    item = Component.objects.get_or_404(id=unquote_plus(id))

    class MetaForm(flask_wtf.Form):
        pass

    def field_id(cls, meta):
        return "{0}_{1}".format(str(cls.id),
                                hashlib.md5(meta.encode("utf-8"))
                                       .hexdigest())

    # build serial form
    for cls in item.classes:
        for meta in cls.metadata:
            setattr(MetaForm, field_id(cls, meta.name),
                    wtf.FloatField("{0} {1} ({2})".format(cls.name, meta.name,
                                                          meta.unit),
                                   [wtf.validators.Required()]))

    # create serial defaults
    default = {}
    for entry in item.metadata:
        for name, value in entry.values.items():
            default[field_id(entry.cls, name)] = value
    default = type("DefaultMetadata", (object, ), default)()

    form = MetaForm(obj=default)

    if form.validate_on_submit():
        # copy serial data to item
        item.metadata = []
        for cls in item.classes:
            entry = ComponentMetadataSpec()
            entry.cls = cls
            entry.values = {}
            for meta in cls.metadata:
                field = getattr(form, field_id(cls, meta.name))
                entry.values[meta.name] = field.data
            item.metadata.append(entry)

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
