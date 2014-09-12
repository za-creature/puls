# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import Benchmark, Component, BenchmarkEntry
from puls import app

import itertools
import numpy


@app.task
def generate_top(cls):
    # create theoretical tests
    theoretical = {}
    for meta in cls.metadata:
        theoretical[meta.name] = Benchmark(name=meta.name,
                                           factor=meta.factor,
                                           exponent=meta.exponent,
                                           weights=meta.weights,
                                           entries=[])

    components = [c for c in Component.objects(classes=cls)]
    for component in components:
        for meta in component.metadata:
            if meta.cls != cls:
                continue
            for key in meta.values:
                entry = BenchmarkEntry(component=component,
                                       score=meta.values[key])
                theoretical[key].entries.append(entry)
    theoretical = theoretical.values()

    # load practical tests
    practical = Benchmark.objects(cls=cls)

    benchmarks = itertools.chain(theoretical, practical)

    # determine system matrix size
    cols = len(components)
    rows = 1
    for benchmark in benchmarks:
        rows += len(benchmark.entries) - 1

    # build overdetermined system
    A = numpy.zeros((rows, cols))
    B = numpy.zeros(rows)

    A[0][0] = 1
    B[0] = 1

    row = 1
    for benchmark in benchmarks:
        prev = None
        for curr in benchmark.entries:
            pass
