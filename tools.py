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

def get_subclasses(module, cls):
    """Yield the classes in module ``mod`` that inherit from ``cls``"""
    for name, obj in inspect.getmembers(module):
        if hasattr(obj, "__bases__") and cls in obj.__bases__:
            yield obj

# [a, [b, [d: None], c, None]]
def module_class_hierarchy(module, cls):
    if not hasattr(cls, "__bases__") or not cls.__bases__:
        return None
    return {module_class_hierarchy(module, sub)
            for sub in get_subclasses(module, cls)}

