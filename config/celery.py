# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from config.databases import MONGODB_SETTINGS, REDIS_SETTINGS

import celery.schedules


# celery configuration
BROKER_URL = "redis://{0}:{1}/{2}".format(REDIS_SETTINGS["host"],
                                          REDIS_SETTINGS["port"],
                                          REDIS_SETTINGS["db"])
CELERY_RESULT_BACKEND = "mongodb://{0}:{1}/".format(MONGODB_SETTINGS["host"],
                                                    MONGODB_SETTINGS["port"])
CELERY_MONGODB_BACKEND_SETTINGS = {"database": MONGODB_SETTINGS["db"],
                                   "max_pool_size": 10}
CELERY_ACCEPT_CONTENT = ["pickle"]
CELERYD_CONCURRENCY = 2
CELERYD_HIJACK_ROOT_LOGGER = False

# monkeypatch task settings here
CELERY_ANNOTATIONS = {
}

# crontab goes here
CELERYBEAT_SCHEDULE = {
    "update-exchange-rate": {
        "task": "puls.tasks.update_exchange",
        "schedule": celery.schedules.crontab(minute=0, hour=12)
    }
}
