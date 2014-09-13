# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import (Benchmark, Component, Target, BenchmarkEntry,
                         ComponentPerformanceSpec)
from puls import app

import itertools
import numpy


@app.task(name="puls.tasks.generate_top")
@app.task
def generate_top(cls):
    # create theoretical tests and component map
    theoretical = {}
    for meta in cls.metadata:
        theoretical[meta.name] = Benchmark(name=meta.name,
                                           unit=meta.unit,
                                           exponent=meta.exponent,
                                           weights=meta.weights,
                                           entries=[])

    components = [c for c in Component.objects(classes=cls)]
    comp_map = {}

    for index, component in enumerate(components):
        comp_map[component.id] = index
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

    # determine system matrix size and premultiply scores
    cols = len(components)
    rows = 1
    for benchmark in itertools.chain(theoretical, practical):
        benchmark.factor_map = {}
        for weight in benchmark.weights:
            benchmark.factor_map[weight.target.id] = weight.value

        for entry in benchmark.entries:
            entry.score **= benchmark.exponent
        rows += len(benchmark.entries) - 1

    # build & solve an overdetermined system for each target
    A = numpy.zeros((rows, cols))
    B = numpy.zeros(rows)

    A[0][0] = B[0] = 1

    for component in components:
        component.score = []

    for target in Target.objects():
        row = 1
        for benchmark in itertools.chain(theoretical, practical):
            factor = benchmark.factor_map[target.id]

            prev = None
            for curr in benchmark.entries:
                if prev:
                    prev_pos = comp_map[prev.component.id]
                    curr_pos = comp_map[curr.component.id]

                    score_normalizer = factor / (curr.score + prev.score)

                    A[row][prev_pos] = curr.score * score_normalizer
                    A[row][curr_pos] = -prev.score * score_normalizer
                    row += 1
                prev = curr

        # normalize scores
        scores = numpy.linalg.lstsq(A, B)[0]

        normal = max(scores)
        value_normal = 0
        for index, score in enumerate(scores):
            component = components[index]
            if component.price > 0.01:
                ratio = score / component.price
                if ratio > value_normal:
                    value_normal = ratio

        for index, score in enumerate(scores):
            component = components[index]
            ratio = score / component.price if component.price > 0.01 else 0
            component.score.append(ComponentPerformanceSpec(
                cls=cls,
                target=target,
                performance=score / normal,
                value=ratio / value_normal
            ))

    # holy shit that was hard
    for component in components:
        component.save()
