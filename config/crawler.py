# coding=utf-8
from __future__ import absolute_import, unicode_literals, division


CRAWLER_SETTINGS = {"tries": 10,
                    "redirects": 10,
                    "delay": 10,
                    "user_agents": open("config/user_agents.txt").readlines(),
                    "timeout": 60}
