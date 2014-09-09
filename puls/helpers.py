# coding=utf-8
"""Symbols exported by this module are imported into the jinja2 environment.
Generally used to write general purpose template helpers.
"""
from __future__ import absolute_import, unicode_literals, division
from puls import app

import jinja2
import flask


def javascript(filename=None):
    """Ensures that the page will load 'filename' as a javascript (do not use
    an extension). This takes care of media versioning, prevents duplicates and
    handles compilation if needed."""
    if not hasattr(flask.g, "scripts"):
        flask.g.scripts = set()

    name = "/static/{0}/js/{1}.js".format(app.config["VERSION"], filename)
    if name in flask.g.scripts:
        return ""
    flask.g.scripts.add(name)
    return jinja2.Markup("<script type=\"text/javascript\" src=\"{0}\">"
                         "</script>".format(name))


def stylesheet(filename=None):
    """Ensures that the page will load 'filename' as a stylesheet (do not use
    an extension). This takes care of media versioning, prevents duplicates and
    handles compilation if needed."""
    if not hasattr(flask.g, "stylesheets"):
        flask.g.stylesheets = set()

    name = "/static/{0}/css/{1}.css".format(app.config["VERSION"], filename)
    if name in flask.g.stylesheets:
        return ""
    flask.g.stylesheets.add(name)
    return jinja2.Markup("<link rel=\"stylesheet\" type=\"text/css\" "
                         "href=\"{0}\"/>".format(name))


def resource(filename):
    """Returns the URL a static resource, including versioning."""
    return "/static/{0}/{1}".format(app.config["VERSION"], filename)


def dateformat(date, format="%a, %d %B %Y, %I:%M %p"):
    return date.strftime(format)
