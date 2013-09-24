#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import inspect


def multicopy(object, number_copies):
    return [copy.deepcopy(object) for i in xrange(number_copies)]

def sign(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0

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
