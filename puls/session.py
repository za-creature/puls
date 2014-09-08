# coding=utf-8
"""DEPRECATED. Session data will in the future be stored locally as signed
MsgPack cookie data. MsgPack is faster than pickle, and more space-efficient.
"""
from __future__ import absolute_import, unicode_literals, division

try:
    import cPickle as pickle
except ImportError:
    import pickle
import werkzeug
import datetime
import flask
import uuid


class RedisSession(werkzeug.datastructures.CallbackDict,
                   flask.sessions.SessionMixin):
    def __init__(self, session_id, data={}):
        def on_change(self):
            self.modified = True
        werkzeug.datastructures.CallbackDict.__init__(self, data, on_change)

        self.id = session_id
        self.modified = False
        self.new = bool(data)


class RedisSessionInterface(flask.sessions.SessionInterface):
    def open_session(self, app, request):
        try:
            session_id = request.cookies[app.session_cookie_name]
            session_data = app.redis.get("session:" + session_id)
            return RedisSession(session_id, pickle.loads(session_data))
        except:
            return RedisSession(str(uuid.uuid4()))

    def save_session(self, app, session, response):
        if session:
            # save session data
            app.redis.setex("session:" + session.id,
                            time=app.permanent_session_lifetime if
                            session.permanent else datetime.timedelta(days=1),
                            value=pickle.dumps(dict(session)))
            response.set_cookie(app.session_cookie_name, session.id,
                                expires=self.get_expiration_time(app, session),
                                httponly=True,
                                domain=self.get_cookie_domain(app))
        else:
            # delete empty session
            app.redis.delete("session:" + session.id)
            response.delete_cookie(app.session_cookie_name,
                                   domain=self.get_cookie_domain(app))
