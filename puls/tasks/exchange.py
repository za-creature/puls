# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Config
from puls import app

import lxml.etree
import requests


@app.task(name="puls.tasks.update_exchange")
def update_exchange():
    # get remote data feed
    response = requests.get("http://bnr.ro/nbrfxrates.xml")
    assert response.status_code == 200

    # parse and split xml
    root = lxml.etree.fromstring(response.content)
    header, body = root
    publisher, date, msg = header
    subject, origin, cube = body

    # sanity checks
    assert publisher.text == "National Bank of Romania"
    assert msg.text == "DR"
    assert date.text == cube.attrib["date"]
    assert subject.text == "Reference rates"
    assert origin.text == "RON"

    rates = {}
    for rate in cube:
        try:
            multiplier = int(rate.attrib["multiplier"])
        except KeyError:
            multiplier = 1
        rates[rate.attrib["currency"]] = multiplier / float(rate.text)

    Config.set("exchange", rates)
