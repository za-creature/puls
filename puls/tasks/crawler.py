# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import crawlers
from puls import app


@app.task(name="puls.tasks.crawl_supplier")
@app.task
def crawl_supplier(supplier):
    crawler_class = getattr(crawlers, supplier.cls)
    assert issubclass(crawler_class, crawlers.SupplierCrawler)
    crawler = crawler_class()
    crawler.run(supplier)
