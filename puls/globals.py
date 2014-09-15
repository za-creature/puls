# coding=utf-8
"""Symbols exported by this module are imported into the puls namespace. Usage:

from puls import <symbol>
"""
from __future__ import absolute_import, unicode_literals, division
from puls.compat import range

import math


class AttributeDict(dict):
    def __getattr__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            raise AttributeError(key)
    __setattr__ = dict.__setattr__
    __delattr__ = dict.__delattr__


class Pagination(object):
    def __init__(self, queryset, page, per_page):
        self.current = page
        self.per_page = per_page

        self.total = queryset.count()

        self.start = (page - 1) * per_page
        self.end = min(self.total, page * per_page)

        self.items = queryset[self.start:self.end]

    def __iter__(self):
        return iter(self.items)

    @property
    def last(self):
        return int(math.ceil(self.total / float(self.per_page)))

    @property
    def prev(self):
        return self.current - 1

    @property
    def has_prev(self):
        return self.current > 1

    @property
    def has_next(self):
        return self.current < self.last

    @property
    def next(self):
        """Number of the next page"""
        return self.current + 1

    def all(self, left_edge=2, left_current=2, right_current=2, right_edge=2):
        last = 0
        for num in range(1, self.last + 1):
            if \
                    num <= left_edge or (
                        num > self.current - left_current - 1 and
                        num < self.current + right_current + 1
                    ) or \
                    num > self.last - right_edge:

                if last + 1 != num:
                    yield None
                yield num
                last = num


def paginate(queryset, page, per_page=20):
    return Pagination(queryset, page, per_page)
