#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import time

Pixel = collections.namedtuple('Pixel', 'x y')
Size = collections.namedtuple('Size', 'width height')
SpecialTuple = collections.namedtuple('SpecialTuple', 'center figure point_number')


def sign(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0

def fpart(num):
    return num - int(num)

def log_exec_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_diff = time.time() - start_time
        print '*** %s: %f' %(func.__name__, time_diff)
        return result
    return wrapper


class StateWatcher:
    def __init__(self, state, on_changed):
        self._state = state
        self._on_changed = on_changed

        self._grabbed_state = None

    def grab(self):
        assert self._grabbed_state is None
        self._grabbed_state = self._state()

    def check(self):
        assert self._grabbed_state is not None
        current_state = self._state()
        if current_state != self._grabbed_state:
            self._on_changed(current_state)
        self._grabbed_state = None

def filtered_items(d, keys):
    """
    >>> dict(filtered_items({1: 10, 2: 20, 3: 30}, [2, 3]))
    {2: 20, 3: 30}
    >>> dict(filtered_items({1: 10, 2: 20, 3: 30}, []))
    {}
    >>> dict(filtered_items({1: 10, 2: 20, 3: 30}, [1, 2, 3]))
    {1: 10, 2: 20, 3: 30}
    >>> dict(filtered_items({1: 10, 2: 20, 3: 30}, [1, 2, 3, 4]))
    {1: 10, 2: 20, 3: 30}
    """
    return (item for item in d.iteritems() if item[0] in keys)

def place_between(number, minimum, maximum):
    """
    >>> place_between(3, 1, 4)
    3
    >>> place_between(0, 1, 4)
    1
    >>> place_between(7, 1, 4)
    4
    """
    if number < minimum:
        return minimum
    elif number > maximum:
        return maximum
    else:
        return number

def max_diff(values):
    """
    >>> max_diff([1, -1, 5])
    6
    >>> max_diff([1, 2, 5])
    4
    """
    return abs(max(values) - min(values))