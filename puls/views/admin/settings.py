# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls import app


@app.route("/admin/settings/")
@app.template("admin/dashboard.html")
@app.logged_in
def account_settings():
    pass
