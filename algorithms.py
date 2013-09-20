#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools

families = {}


def algorithm(points, family, name):
    def wrap(func):
        func.points_number = points

        family_dict = families.setdefault(family, dict())
        family_dict[name] = func

        return func
    return wrap


@algorithm(points=1, family=u'Точка', name=u'точка')
def dot(draw_func, point):
    draw_func(point.x, point.y)


@algorithm(points=2, family=u'Отрезок', name=u'ЦДА')
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

@algorithm(points=2, family=u'Отрезок', name=u'Алгоритм Брезенхема')
def brezen(draw_func, point1, point2):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x, y = x1, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    e = float(y2 - y1) / (x2 - x1) - 0.5

    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1

    i = 0
    while i <= dx:
        draw_func(x, y)
        if e >= 0:
            y += signY
            e -= 2 * dx
        else:
            x += signX
            e += 2 * dy
            i += 1