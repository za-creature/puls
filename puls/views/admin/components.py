# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import (Component, ComponentForm, ComponentMetadataSpec,
                         Connector, Bus, Supplier, ExternalComponent)
from puls.compat import unquote_plus, str
from puls import app, paginate, AttributeDict

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


@app.route("/admin/components/search/external/<id>")
@app.logged_in
def search_external_components(id):
    supplier = Supplier.objects.get_or_404(id=unquote_plus(id))
    term = flask.request.args.get("term", "")
    if term:
        results = ExternalComponent.search(term, supplier.id)
    else:
        results = ExternalComponent.objects(supplier=supplier.id).limit(100)

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

    external_references = []
    matched_suppliers = set()
    if item:
        for external in item.external:
            matched_suppliers.add(external.supplier)
            external_references.append({"supplier": external.supplier,
                                        "component": external})
    for supplier in Supplier.objects:
        if supplier not in matched_suppliers:
            external_references.append({"supplier": supplier,
                                        "component": None})

    if form.validate_on_submit():
        if not item:
            item = Component()
        form.populate_obj(item)

        # add connectors
        item.connectors = []
        counts = flask.request.form.getlist("counts")
        for key, value in enumerate(flask.request.form.getlist("buses")):
            bus = Bus.objects.get_or_404(id=value)
            try:
                count = int(counts[key])
                if count < -10 or count > 10:
                    raise ValueError
            except (ValueError, IndexError):
                flask.abort(404)
            item.connectors.append(Connector(bus=bus, count=count))

        # add external components
        item.external = []
        for id in flask.request.form.getlist("external"):
            if id:
                external = ExternalComponent.objects.get_or_404(id=id)
                item.external.append(external)

        item.save()
        flask.flash("The component was saved. Please update the metadata "
                    "if new classes were added", "success")
        return flask.redirect(flask.url_for("edit_component_meta",
                                            id=str(item.id)))

    return {"form": form,
            "item": item,
            "external": external_references}


@app.route("/admin/components/<id>/meta/", methods=["GET", "POST"])
@app.template("admin/components/metadata.html")
@app.logged_in
def edit_component_meta(id=None):
    item = Component.objects.get_or_404(id=unquote_plus(id))

    class MetaForm(flask_wtf.Form):
        pass

    def field_id(cls, meta):
        return "f{0}_{1}".format(str(cls.id),
                                 hashlib.md5(meta.encode("utf-8"))
                                        .hexdigest())

    # build serial form
    for cls in item.classes:
        for meta in cls.metadata:
            field = wtf.FloatField("{0} {1}".format(cls.name, meta.name),
                                   [wtf.validators.Required()])
            setattr(MetaForm, field_id(cls, meta.name), field)

    # create serial defaults
    default = AttributeDict()
    for entry in item.metadata:
        for name, value in entry.values.items():
            default[field_id(entry.cls, name)] = value

    # wtforms is gay
    form = MetaForm(obj=default)
    for cls in item.classes:
        for meta in cls.metadata:
            getattr(form, field_id(cls, meta.name)).unit = meta.unit

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
