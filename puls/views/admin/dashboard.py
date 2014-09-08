# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls import app


@app.route("/admin/")
@app.template("admin/dashboard.html")
@app.logged_in
def dashboard():
    pass
