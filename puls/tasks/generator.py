# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import (Benchmark, Component, Target, BenchmarkEntry,
                         ComponentPerformanceSpec, Class)
from puls import app

import itertools
import heapq
import random
import numpy


class System(object):
    def __init__(self, target, component):
        if isinstance(component, Component):
            # fork constructor
            self.target = target.target
            self.budget = target.budget

            # add component, price and power requirements
            self.components = target.components[:]
            self.components.append(component)
            self.price = target.price + component.price
            self.power = target.power - component.power

            # update class spec
            self.classes = target.classes.copy()
            for cls in component.classes:
                self.classes.add(cls.id)

            # update connector count
            self.buses = target.buses.copy()
            for connector in component.connectors:
                self.add_bus(connector)

            # update performance characteristic
            for score in component.score:
                if score.target == self.target:
                    for weight in score.cls.weights:
                        if weight.target == self.target:
                            weight = weight.value
                            break
                    else:
                        raise ValueError("Target not found in class weights")

                    self.performance = (target.performance +
                                        score.performance * weight)
                    break
            else:
                raise ValueError("Target not found in component performance")
        else:
            # default constructor (component is the max budget)
            self.target = target
            self.budget = component

            self.components = []
            self.price = 0
            self.power = 0

            self.classes = set()
            self.buses = {}
            self.performance = 0

    def bus_count(self, connector):
        return self.buses.get(connector.bus.id, 0)

    def add_bus(self, connector):
        self.buses[connector.bus.id] = self.bus_count(connector) + \
                                       connector.count

    def compatible_with(self, component):
        # connector check
        for connector in component.connectors:
            if self.bus_count(connector) + connector.count < 0:
                return False

        # power check
        if self.power - component.power < 0:
            return False

        # price check
        if self.price + component.price > self.budget:
            return False

        # duplicate PSU check
        if self.power > 0 and component.power < 0:
            return False

        # all tests pass
        return True


class BoundedHeap(object):
    def __init__(self, count):
        self.data = []
        self.count = count

    def score(self, item):
        raise NotImplemented

    def add(self, item):
        score = self.score(item)
        if len(self.data) < self.count:
            # heap is empty, add unconditionally
            heapq.heappush(self.data, (score, item))
        else:
            # heap is full
            if score < self.data[0][0]:
                # ... but the current item is worse than the worst item
                # return the current item to allow it to be added to another
                # heap
                return item
            else:
                # ... and the current item is better than the worst item
                # evict the worst item, granting it's slot to the current item
                # return the worst item to allow it to be added to another heap
                return heapq.heappushpop(self.data, (score, item))[1]


class PerformanceHeap(BoundedHeap):
    def score(self, item):
        return -item.performance


class AffordableHeap(BoundedHeap):
    def score(self, item):
        return -item.price


class ValueHeap(BoundedHeap):
    def score(self, item):
        return item.price / item.performance


@app.task(name="puls.tasks.generate_system")
@app.task
def generate_system(target, budget):
    components = {}

    # build component map
    for component in Component.objects:
        for cls in component.classes:
            if cls.id not in components:
                components[cls.id] = []
            components[cls.id].append(component)

    heaps = []
    def update_heaps(system):
        for heap in heaps:
            system = heap.add(system)
            if system is None:
                break

    null = None
    for cls in Class.objects.order_by("priority"):
        if cls.id not in components:
            continue

        systems = itertools.chain(*[heap.data for heap in heaps])
        if not systems:
            raise ValueError("No results found")

        heaps[:] = [PerformanceHeap(5000), AffordableHeap(5000),
                    ValueHeap(5000)]
        if null:
            # attempt to add a component of type `cls` to all existing systems
            for _, old_system in systems:
                if cls.id in old_system.classes:
                    # old system already has a component with this class, so
                    # attempt to remember it
                    update_heaps(old_system)

                for component in components[cls.id]:
                    if old_system.compatible_with(component):
                        system = System(old_system, component)
                        update_heaps(system)
        else:
            # bootstrap the most prioritary class
            null = System(target, budget)
            for component in components[cls.id]:
                system = System(null, component)
                update_heaps(system)

    max = 0
    best = None
    for _, system in itertools.chain(*[heap.data for heap in heaps]):
        if system.performance > max:
            max = system.performance
            best = system

    return best
