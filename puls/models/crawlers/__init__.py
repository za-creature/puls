# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import ExternalComponent
from puls import app

import collections
import importlib
import traceback
import requests
import pkgutil
import random
import time


class SupplierCrawler(object):
    def __init__(self):
        """Called to initialize the crawler."""
        self.http = requests.Session()
        self.http.max_redirects = app.config["CRAWLER_SETTINGS"]["redirects"]

        self.http.headers["user-agent"], = random.sample(
            app.config["CRAWLER_SETTINGS"]["user_agents"], 1)
        self.delay = app.config["CRAWLER_SETTINGS"]["delay"]

        self.queue = collections.deque()
        self.referrer = None

    def run(self, supplier):
        self.supplier = supplier
        while self.queue:
            # get the most outstanding request from the queue and execute it,
            # making sure to update the referrer header for the next request
            url, data = self.queue.popleft()
            tries = app.config["CRAWLER_SETTINGS"]["tries"]
            while tries:
                try:
                    print("GET {0}".format(url))
                    r = requests.get(
                        url,
                        headers={"referer": self.referrer},
                        timeout=app.config["CRAWLER_SETTINGS"]["timeout"])
                except requests.RequestException as e:
                    print("Got {0} while loading {1}".format(
                        e.__class__.__name__, url))
                else:
                    self.referrer = r.url

                    if r.status_code == 200:
                        # request was successful; delegate page processing to
                        # subclass and stop processing
                        try:
                            self.handle(r.text, data)
                        except Exception:
                            print("An unhandled exception occurred"
                                  " while processing {0}".format(url))
                            traceback.print_exc()
                        tries = 0

                    elif r.status_code // 100 == 5:
                        # some sort of server error; try again later if the
                        # retry limit is not exceeded
                        print("Received {0} response while loading "
                              "{1}.".format(r.status_code, url))
                        tries -= 1

                    else:
                        # unsupported response status code; ignore but log
                        print("Unexpected {0} response code occurred "
                              "while loading {1}".format(r.status_code, url))
                        tries = 0

                # sleep until the next request is performed; to ensure
                # human-like behavior, the sleep duration is a uniformly
                # distributed variable between 1/2 and 3/2 of the sleep
                # duration
                time.sleep(random.uniform(self.delay / 2, 3 * self.delay / 2))

    def enqueue(self, url, data=None, first=False):
        if first:
            self.queue.appendleft((url, data))
        else:
            self.queue.append((url, data))

    def found(self, _id, name, price, stock, url):
        print("Found component {0}".format(name.encode("ascii", "ignore")))
        ExternalComponent.objects(supplier=self.supplier,
                                  identifier=_id) \
                         .update_one(upsert=True,
                                     set__name=name[:256],
                                     set__price=price,
                                     set__stock=stock,
                                     set__url=url)

    def handle(self, body, data):
        raise Exception("Please override {0}.handle".format(
            self.__class__.__name__))


# import submodule symbols in self
for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module("{0}.{1}".format(__name__, name))
    try:
        symbols = module.__all__
    except AttributeError:
        symbols = filter(lambda name: not name.startswith("_"), dir(module))

    for name in symbols:
        if name not in globals():
            globals()[name] = getattr(module, name)
