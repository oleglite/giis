#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import time

Pixel = collections.namedtuple('Pixel', 'x y')
Size = collections.namedtuple('Size', 'width height')


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
        func(*args, **kwargs)
        time_diff = time.time() - start_time
        print '*** %s: %f' %(func.__name__, time_diff)
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