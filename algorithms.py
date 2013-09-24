#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import plot

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
    draw_func(point)


@algorithm(points=2, family=u'Отрезок', name=u'ЦДА')
def DDA(draw_func, point1, point2):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y

    length = max(abs(x2 - x1), abs(y2 - y1))
    if length <= 0:
        length = 1

    dx = float(x2 - x1) / length
    dy = float(y2 - y1) / length

    x = x1
    y = y1

    for i in xrange(int(length) + 1):
        draw_func(plot.Point(int(round(x)), int(round(y))))
        x += dx
        y += dy

@algorithm(points=2, family=u'Отрезок', name=u'Алгоритм Брезенхема')
def bresenham(draw_func, point1, point2):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x, y = x1, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    e = 2 * (y2 - y1) - (x2 - x1)

    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1

    i = 0
    while i <= dx:
        #a = 1 / (1 + abs(e) / float(dx + dy))
        draw_func(plot.Point(int(x), int(y)))
        if e >= 0:
            y += signY
            e -= 2 * dx
        else:
            x += signX
            e += 2 * dy
            i += 1