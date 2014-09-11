# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.tasks import suppliers
from puls import app

@app.task
def update_supplier(supplier):
    crawler_class = getattr(suppliers, supplier.cls)
    assert issubclass(crawler_class, suppliers.Supplier)
    crawler = crawler_class()
    crawler.run(supplier)
