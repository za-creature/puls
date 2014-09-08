# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.globals import *  # noqa

import flask.ext.mongoengine
import flask_wtf
import logging
import celery
import redis
import flask
import os


# initialize logging
logging.basicConfig(level=logging.DEBUG)


# initialize app
class Puls(flask.Flask):
    jinja_options = dict(flask.Flask.jinja_options,
                         extensions=["puls.htmlcompress.HTMLCompress"],
                         finalize=lambda x: x if x is not None else "")


app = Puls(__name__,
           static_url_path="/static",
           static_folder=os.path.abspath("static"),
           template_folder=os.path.abspath("templates"))
app.config.from_object("config")
app.csrf = flask_wtf.csrf.CsrfProtect(app)


# initialize task queue
celery = celery.Celery(app.import_name)
celery.config_from_object("config")


class PulsTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return celery.Task.__call__(self, *args, **kwargs)

celery.Task = PulsTask
app.task = celery.task


# connect to databases
app.redis = redis.StrictRedis(**app.config["REDIS_SETTINGS"])
app.db = flask.ext.mongoengine.MongoEngine(app)


# import decorators into the application
import puls.decorators
for name in dir(puls.decorators):
    item = getattr(puls.decorators, name)
    if callable(item):
        setattr(app, name, item)


# import template helpers as jinja superglobals
import puls.helpers
for name in dir(puls.helpers):
    item = getattr(puls.helpers, name)
    if callable(item):
        app.jinja_env.globals[name] = item


# prepare session handler
import puls.session
app.session_interface = puls.session.RedisSessionInterface()


# import views to create routing table
import puls.views  # noqa

# import tasks to create task registry
import puls.tasks  # noqa
