# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls import app

import importlib
import pkgutil
import flask


# configure versioned static path
@app.route("/static/<int:version>/<path:static_file>")
def versioned_static(version, static_file):
    # not going to hell; not going to hell; not going to hell
    return app.test_client().get("/static/" + static_file,
                                 headers=list(flask.request.headers))


# configure legacy favicon path
@app.route("/favicon.ico")
def favicon():
    return app.test_client().get("/static/img/favicon.ico",
                                 headers=list(flask.request.headers))


# configure legacy apple-touch-icon path
@app.route("/apple-touch-icon.png")
def touch_icon():
    return app.test_client().get("/static/img/favicon.png",
                                 headers=list(flask.request.headers))


# import all submodules
for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    importlib.import_module("{0}.{1}".format(__name__, name))
