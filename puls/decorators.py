# coding=utf-8
"""Symbols exported by this module are imported into the puls web application.
Generally used for common functionality shared between HTTP request handlers.
"""
from __future__ import absolute_import, unicode_literals, division

import functools
import werkzeug
import flask


def template(filename):
    """Decorates a function to render a template, using the returned dict as
    the context. The behavior can be overridden by returning a Response object,
    in which case the decorator does nothing."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            context = f(*args, **kwargs)
            if isinstance(context, (flask.Response, werkzeug.Response)):
                return context
            if not isinstance(context, dict):
                context = {}
            return flask.render_template(filename, **context)
        return wrapper
    return decorator


def logged_in(f):
    """Decorates a function to check that a user is signed in prior to the
    call. If the user is not signed in and a GET request was attempted, a
    redirect is performed to the login page. If the user is signed in but does
    not have the specified permission, or if the request is a POST request,
    then a generic 403 page is returned informing the user of the situation."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in flask.session:
            if flask.request.method == "GET":
                flask.session["after_login"] = flask.request.url
                return flask.redirect(flask.url_for("login"))
        else:
            return f(*args, **kwargs)
        flask.abort(403)
    return wrapper


def has_main_menu(f):
    """Decorates a function to add the variables that are required by the Puls
    main menu. The behavior can be overridden by returning a Response object,
    in which case the decorator does nothing."""
    from puls.models import Component, Manufacturer, Supplier

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        context = f(*args, **kwargs)
        if isinstance(context, (flask.Response, werkzeug.Response)):
            return context
        if not isinstance(context, dict):
            context = {}
        context.update({
            "component_count": Component.objects().count(),
            "manufacturer_count": Manufacturer.objects().count(),
            "supplier_count": Supplier.objects().count()
        })
        return context
    return wrapper
