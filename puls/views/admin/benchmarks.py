# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Benchmark, BenchmarkForm
from puls import app

import urllib
import flask


@app.route("/admin/benchmarks/")
@app.template("admin/benchmarks/list.html")
@app.logged_in
def manage_benchmarks():
    return {"items": Benchmark.objects.filter()}


@app.route("/admin/benchmarks/new", methods=["GET", "POST"],
           endpoint="add_benchmark")
@app.route("/admin/benchmarks/<id>/edit", methods=["GET", "POST"])
@app.template("admin/benchmarks/form.html")
@app.logged_in
def edit_benchmark(id=None):
    if id is None:
        item = None
    else:
        try:
            item = Benchmark.objects.get(id=urllib.unquote_plus(id))
        except Benchmark.DoesNotExist:
            return flask.abort(404)

    form = BenchmarkForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = Benchmark()
        form.populate_obj(item)
        item.save()
        flask.flash("The benchmark was saved", "success")
        return flask.redirect(flask.url_for("manage_benchmarks"))

    return {"form": form,
            "item": item}


@app.route("/admin/benchmarks/<id>/delete/")
@app.logged_in
def delete_benchmark(id):
    try:
        item = Benchmark.objects.get(id=urllib.unquote_plus(id))

        item.delete()
        flask.flash("Your benchmark has been deleted!", "warning")
        return flask.redirect(flask.url_for("manage_benchmarks"))
    except Benchmark.DoesNotExist:
        return flask.abort(404)
