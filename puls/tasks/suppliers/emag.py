# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.tasks.suppliers import Supplier

import bs4
try:
    import urllib.parse as urlparse
    assert urlparse
except ImportError:
    import urlparse


class EMag(Supplier):
    abstract = False

    def __init__(self):
        super(EMag, self).__init__()

        for args in (
            ("http://www.emag.ro", False),  # load homepage
            ("http://www.emag.ro/componente/l", False),  # switch to components
            ("http://www.emag.ro/hard_disk-uri/c", False),  # follow hdd link
            ("http://www.emag.ro/hard_disk-uri/c?ref=grid", True),  # grid on
            ("http://www.emag.ro/solid-state_drive_ssd_/c", True),
            ("http://www.emag.ro/procesoare/c", True),
            ("http://www.emag.ro/placi_video/c", True),
            ("http://www.emag.ro/placi_baza/c", True),
            ("http://www.emag.ro/memorii/c", True),
            ("http://www.emag.ro/carcase/c", True),
            ("http://www.emag.ro/surse/c", True),
            ("http://www.emag.ro/placi_sunet/c", True),
            ("http://www.emag.ro/dvd-writer/c", True),
            ("http://www.emag.ro/blu-ray/c", True),
        ):
            self.enqueue(*args)

    def handle(self, body, valid):
        if not valid:
            return

        page = bs4.BeautifulSoup(body, "lxml")

        failed = True
        for product in page.select("div.product-holder-grid"):
            failed = False

            # id
            uniq = product.select("input[type=hidden]")[0]["value"]

            # name & url
            anchor = product.select("h2 > a")[0]
            name = anchor["title"]
            url = urlparse.urljoin("http://www.emag.ro", anchor["href"])

            # price
            m_int = product.select("span.money-int")[0].text.replace(".", "")
            m_float = product.select("sup.money-decimal")[0].text
            price = int(m_int) + float(m_float) / 100

            # stock
            stock = product.select("span.stare-disp-listing")[0].text.strip() \
                not in ("La comandă", "Momentan indisponibil", "Stoc epuizat")

            self.found(uniq, name, price, stock, url)

        if failed:
            raise Exception("No components found")

        # determine next page, if any
        pages = page.select("div.products-pagination")
        if not pages:
            return
        current = pages[len(pages) - 1].select("span.pg.selected")
        if not current:
            return
        next = current[0].find_next_siblings("a")
        if not next:
            return
        self.enqueue(
            urlparse.urljoin("http://www.emag.ro", next[0]["href"]),
            True, True
        )
