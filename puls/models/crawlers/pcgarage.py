# coding=utf8
from __future__ import absolute_import, unicode_literals, division
from puls.models.crawlers import SupplierCrawler
from puls.compat import urlparse

import bs4
import re


class PCGarage(SupplierCrawler):
    abstract = False

    def __init__(self):
        super(PCGarage, self).__init__()

        for args in (
            ["http://www.pcgarage.ro/", False],
            ["http://www.pcgarage.ro/placi-de-baza/", True],
            ["http://www.pcgarage.ro/hard-disk-uri/", True],
            ["http://www.pcgarage.ro/ssd/", True],
            ["http://www.pcgarage.ro/procesoare/", True],
            ["http://www.pcgarage.ro/placi-video/", True],
            ["http://www.pcgarage.ro/memorii/", True],
            ["http://www.pcgarage.ro/carcase/", True],
            ["http://www.pcgarage.ro/surse/", True],
            ["http://www.pcgarage.ro/placi-de-sunet/", True],
            ["http://www.pcgarage.ro/dvd-writere/", True],
            ["http://www.pcgarage.ro/unitati-optice-blu-ray/", True],
        ):
            self.enqueue(*args)

    def handle(self, body, valid):
        if not valid:
            return

        page = bs4.BeautifulSoup(body, "lxml")

        failed = True
        for product in page.select("div.product-box-container"):
            failed = False

            # id
            uniq = re.sub(
                "[^\d]", "",
                product.select("div.pb-compare input[type=checkbox]")[0]["id"]
            )

            # name & url
            anchor = product.select("div.pb-name a")[0]
            name = anchor["title"]
            url = urlparse.urljoin("http://www.pcgarage.ro", anchor["href"])

            # price
            match = re.match(
                "([\d\.]+),(\d+)",
                product.select("div.pb-price p")[0].string
            )
            price = int(match.group(1).replace(".", "")) + \
                float(match.group(2)) / 100

            # stock
            availability = product.select("div.pb-availability")[0]["class"]
            stock = "instock" in availability or \
                "insupplierstock" in availability

            self.found(uniq, name, price, stock, url)

        if failed:
            raise Exception("No components found")

        # determine next page, if any
        current = page.select("div.lr-pagination ul li span")
        if current:
            current = current[0].parent
            next = current.find_next_sibling("li")
            if next:
                self.enqueue(
                    urlparse.urljoin("http://www.pcgarage.ro", next.a["href"]),
                    True, True
                )
