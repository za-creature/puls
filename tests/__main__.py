#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, unicode_literals, division

# fix import path
import sys
import os
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.getcwd())

from puls.tasks import suppliers

import codecs


def runtest(cls, fixture):
    results = []
    queue = []

    def test_component(_id, name, price, stock, url):
        results.append(_id)
        assert len(_id) < 32, "ID too long"
        assert isinstance(price, float), "Price must be floating point"
        assert price > 0, "Price must be positive"
        assert isinstance(stock, bool), "Stock must be True or False"
        assert len(url) < 256, "URL too long"

    handler = cls()
    handler.found = test_component
    handler.enqueue = lambda u, d, f=False: queue.append(u)

    handler.handle(codecs.open(fixture, "rb", "utf-8").read(), True)

    assert results, "No components found"
    assert len(results) == 40, "Partial resultset found"
    assert queue, "No follow up page found"
    assert len(queue) == 1, "Multiple follow up pages"


runtest(suppliers.EMag, "tests/fixtures/emag.html")
