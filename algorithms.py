#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools


def points_number(number):
    """
    >>> def foo(x, y):
    ...     print x, y
    ...
    >>> foo = points_number(3)(foo)
    >>> foo(1, 2)
    1 2
    >>> foo.points_number
    3
    """
    def wrap(func):
        func.points_number = number
        return func
    return wrap


@points_number(1)
def dot(draw_func, point):
    draw_func(point.x, point.y)


@points_number(2)
def CDA(draw_func, point1, point2):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y

    length = max(abs(x2 - x1), abs(y2 - y1))
    if not length:
        length = 1

    dx = float(x2 - x1) / length
    dy = float(y2 - y1) / length

    x = x1 + 0.5 * tools.sign(dx)
    y = y1 + 0.5 * tools.sign(dy)

    for i in xrange(int(length) + 1):
        draw_func(x, y)
        x += dx
        y += dy