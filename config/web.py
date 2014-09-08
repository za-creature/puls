# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

import datetime

MAX_CONTENT_LENGTH = 256 * 1024 * 1024
JSON_AS_ASCII = False

# session configuration
SECRET_KEY = "K|(!*N>Q+(/]v:)nFMmX>B1+>$D0+~PD|&U^xM&#KN!-q,3~Y-XpIz[Q9Vhi^{z."
SESSION_COOKIE_NAME = "session"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
REMEMBER_COOKIE_DURATION = PERMANENT_SESSION_LIFETIME
