# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Target, Targets, TargetForm
from puls.compat import unquote_plus, str
from puls import app, paginate

import flask


@app.route("/admin/targets/", endpoint="manage_targets")
@app.route("/admin/targets/<int:page>/")
@app.template("admin/targets/list.html")
@app.logged_in
def list_targets(page=1):
    return {"page": paginate(Target.objects, page, 20)}


@app.route("/admin/targets/search/")
@app.logged_in
def search_targets():
    query = flask.request.args.get("term", "")
    return flask.jsonify({"results": [{
        "id": str(item["_id"]),
        "text": str(item["name"])
    }
        for item in Targets.find({"$text": {"$search": query}},
                                 {"score": {"$meta": "textScore"}})
                           .sort([("score", {"$meta": "textScore"})])
                           .limit(100)
    ]})


@app.route("/admin/targets/new", methods=["GET", "POST"],
           endpoint="add_target")
@app.route("/admin/targets/<id>/edit", methods=["GET", "POST"])
@app.template("admin/targets/form.html")
@app.logged_in
def edit_target(id=None):
    if id is None:
        item = None
    else:
        item = Target.objects.get_or_404(id=unquote_plus(id))

    form = TargetForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Target()
        form.populate_obj(item)
        item.save()
        flask.flash("The target was saved", "success")
        return flask.redirect(flask.url_for("manage_targets"))

    return {"form": form,
            "item": item}


@app.route("/admin/targets/<id>/delete/")
@app.logged_in
def delete_target(id):
    item = Target.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your target has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_targets"))
