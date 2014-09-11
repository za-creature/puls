# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Benchmark, BenchmarkForm
from puls.compat import unquote_plus
from puls import app, paginate

import flask


@app.route("/admin/benchmarks/", methods=["GET", "POST"],
           endpoint="manage_benchmarks")
@app.route("/admin/benchmarks/<int:page>/")
@app.template("admin/benchmarks/list.html")
@app.logged_in
def list_benchmarks(page=1):
    term = flask.request.form.get("term", "")
    if term:
        page = Benchmark.search(term)
    else:
        page = paginate(Benchmark.objects, page, 20)
    return {"term": term,
            "page": page}


@app.route("/admin/benchmarks/search/")
@app.logged_in
def search_benchmarks():
    term = flask.request.args.get("term", "")
    if term:
        results = Benchmark.search(term)
    else:
        results = Benchmark.objects.limit(100)

    return flask.jsonify({"results": [{"id": str(item.id),
                                       "text": str(item.name)}
                                      for item in results]})


@app.route("/admin/benchmarks/new/", methods=["GET", "POST"],
           endpoint="add_benchmark")
@app.route("/admin/benchmarks/<id>/edit/", methods=["GET", "POST"])
@app.template("admin/benchmarks/form.html")
@app.logged_in
def edit_benchmark(id=None):
    if id is None:
        item = None
    else:
        item = Benchmark.objects.get_or_404(id=unquote_plus(id))

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
    item = Benchmark.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your benchmark has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_benchmarks"))
