# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import (Benchmark, BenchmarkForm, BenchmarkEntry,
                         BenchmarkEntryForm)
from puls.compat import unquote_plus, str
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
        return flask.redirect(flask.url_for("manage_benchmark_entries",
                                            id=str(item.id)))

    return {"form": form,
            "item": item}


@app.route("/admin/benchmarks/<id>/delete/")
@app.logged_in
def delete_benchmark(id):
    item = Benchmark.objects.get_or_404(id=unquote_plus(id))
    item.delete()

    flask.flash("Your benchmark has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_benchmarks"))


@app.route("/admin/benchmarks/<id>/entries/")
@app.template("admin/benchmarks/components/list.html")
@app.logged_in
def manage_benchmark_entries(id):
    bench = Benchmark.objects.get_or_404(id=unquote_plus(id))
    return {"bench": bench}


@app.route("/admin/benchmarks/<id>/entries/new/", methods=["GET", "POST"],
           endpoint="add_benchmark_entry")
@app.route("/admin/benchmarks/<id>/entries/<component>/edit/",
           methods=["GET", "POST"])
@app.template("admin/benchmarks/components/form.html")
@app.logged_in
def edit_benchmark_entry(id, component=None):
    bench = Benchmark.objects.get_or_404(id=unquote_plus(id))
    if component is None:
        item = None
    else:
        component = unquote_plus(component)
        for index, entry in enumerate(bench.entries):
            if str(entry.component.id) == component:
                item = entry
                break
        else:
            flask.abort(404)

    form = BenchmarkEntryForm(obj=item)

    if form.validate_on_submit():
        if not item:
            item = BenchmarkEntry()
            bench.entries.append(item)
            index = -1

        form.populate_obj(bench.entries[index])
        bench.save()
        flask.flash("The benchmark entry was saved", "success")
        return flask.redirect(flask.url_for("manage_benchmark_entries",
                                            id=str(bench.id)))

    return {"form": form,
            "item": item,
            "bench": bench}


@app.route("/admin/benchmarks/<id>/entries/<component>/delete/")
@app.logged_in
def delete_benchmark_entry(id, component):
    bench = Benchmark.objects.get_or_404(id=unquote_plus(id))
    component = unquote_plus(component)
    for index, entry in enumerate(bench.entries):
        if str(entry.component.id) == component:
            break
    else:
        flask.abort(404)

    bench.entries.pop(index)
    bench.save()
    flask.flash("The benchmark entry has been deleted!", "warning")
    return flask.redirect(flask.url_for("manage_benchmark_entries",
                                        id=str(bench.id)))
