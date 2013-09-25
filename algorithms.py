#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import plot

families = {}


def algorithm(points, family, name):
    def wrap(func):
        func.points_number = points
        func.family = family
        func.name = name

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
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1

    error = dx - dy
    while x1 != x2 or y1 != y2:
        draw_func(plot.Point(x1, y1))
        error2 = error * 2
        if error2 > -dy:
            error -= dy
            x1 += signX
        if error2 < dx:
            error += dx
            y1 += signY
    draw_func(point2)

@algorithm(points=2, family=u'Отрезок', name=u'Алгоритм Ву')
def wu(draw_func, point1, point2):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1
    gradientY = float(dy) / dx if dx else 1
    gradientX = float(dx) / dy if dy else 1

    if dx > dy:
        for x in xrange(x1, x2 + signX, signX):
            y = y1 + abs(x - x1) * gradientY * signY
            y_pos = tools.fpart(y)
            draw_func(plot.Point(x, int(y)), (1 - y_pos))
            draw_func(plot.Point(x, int(y) + 1), y_pos)
    else:
        for y in xrange(y1, y2 + signY, signY):
            x = x1 + abs(y - y1) * gradientX * signX
            x_pos = tools.fpart(x)
            draw_func(plot.Point(int(x), y), (1 - x_pos))
            draw_func(plot.Point(int(x) + 1, y), x_pos)