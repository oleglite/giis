#!/usr/bin/env python
# -*- coding: utf-8 -*-
from plot import figure

import tools
from tools import Pixel
import collections
import reflections

by_name = collections.OrderedDict()


def algorithm(name, figure_cls):
    def wrap(func):
        func.NAME = name
        func.Figure = figure_cls
        by_name[name] = func
        return func
    return wrap


@algorithm(name=u'ЦДА', figure_cls=figure.Line)
def DDA(draw_func, figure):
    point1, point2 = figure.points
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
        pixel = Pixel(int(round(x)), int(round(y)))
        draw_func(pixel)
        x += dx
        y += dy


@algorithm(name=u'Алгоритм Брезенхема', figure_cls=figure.Line)
def bresenham(draw_func, figure):
    point1, point2 = figure.points
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1

    error = dx - dy
    while x1 != x2 or y1 != y2:
        draw_func(Pixel(x1, y1))
        error2 = error * 2
        if error2 > -dy:
            error -= dy
            x1 += signX
        if error2 < dx:
            error += dx
            y1 += signY
    draw_func(point2)

@algorithm(name=u'Алгоритм Ву', figure_cls=figure.Line)
def wu(draw_func, figure):
    point1, point2 = figure.points
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1

    if not dx:
        for y in xrange(y1, y2 + signY, signY):
            draw_func(Pixel(x1, y))
        return

    if not dy:
        for x in xrange(x1, x2 + signX, signX):
            draw_func(Pixel(x, y1))
        return

    gradientY = float(dy) / dx
    gradientX = float(dx) / dy

    if dx > dy:
        for x in xrange(x1, x2 + signX, signX):
            y = y1 + abs(x - x1) * gradientY * signY
            y_pos = tools.fpart(y)
            draw_func(Pixel(x, int(y)), (1 - y_pos))
            draw_func(Pixel(x, int(y) + 1), y_pos)
    else:
        for y in xrange(y1, y2 + signY, signY):
            x = x1 + abs(y - y1) * gradientX * signX
            x_pos = tools.fpart(x)
            draw_func(Pixel(int(x), y), (1 - x_pos))
            draw_func(Pixel(int(x) + 1, y), x_pos)

@algorithm(name=u'Алгоритм Брезенхема для окружности', figure_cls=figure.Circle)
def bresenham_circle(draw_func, circle):
    reflector = reflections.Reflector(draw_func)
    h_line = figure.Line([circle.points[0], Pixel(circle.x0 + circle.R, circle.y0)])
    reflector.append(reflections.LineReflection(h_line))
    reflector.append(reflections.PointReflection(circle.points[0]))

    x, y = 0, circle.R
    di = 0#2 - 2 * circle.R

    while y >= 0:
        p = Pixel(x + circle.x0, int(y) + circle.y0)
        reflector.draw_func(p)

        h_incr = 2 * x + 1
        v_incr = -2 * y + 1
        d_incr = 2 * (x - y + 1)

        dh = di + h_incr
        dv = di + v_incr
        dd = di + d_incr

        if dd < 0:
            delta = 2 * (dd + y) - 1
            if delta <= 0:
                x += 1
                di += h_incr
            else:
                x += 1
                y -= 1
                di += d_incr
        elif dd > 0:
            delta = 2 * (dd - x) - 1
            if delta <= 0:
                x += 1
                y -= 1
                di += d_incr
            else:
                y -= 1
                di += v_incr
        else:
            x += 1
            y -= 1
            di += d_incr

@algorithm(name=u'Парабола', figure_cls=figure.Parabola)
def bres_like_parabola(draw_func, parabola):
    x, y0 = parabola.points[0]
    y = 0

    p = abs(parabola.params['p'])
    x_max = parabola.params['scene_size'].width

    di = 0
    increment = tools.sign(parabola.params['p'])

    draw_func(parabola.points[0])

    while 0 < x < x_max:
        dh = di + 2 * p
        dv = di - 1 - 2 * y
        dd = di + 2 * (p - y) - 1

        if dd < 0:
            delta = abs(dh) - abs(dd)
            if delta <= 0:
                x += increment
                di += 2 * p
            else:
                x += increment
                y += 1
                di += 2 * (p - y) - 1
        elif dd > 0:
            delta = abs(dd) - abs(dv)
            if delta <= 0:
                x += increment
                y += 1
                di += 2 * (p - y) - 1
            else:
                y += 1
                di += -1 - 2 * y
        else:
            x += increment
            y += 1
            di += 2 * (p - y) - 1

        draw_func(Pixel(x, y0 + y))
        draw_func(Pixel(x, y0 - y))

@algorithm(u'Метод Эрмита', figure.Curve)
def ermit_curve(draw_func, curve):
    p1x, p1y = curve.points[0]
    p4x, p4y = curve.points[1]
    r1x, r1y = curve.points[2]
    r4x, r4y = curve.points[3]

    t = 0.0
    steps_number = max(abs(p1x - p4x), abs(p1y - p4y), abs(r1x - r4x), abs(r1y - r4y))
    t_incr = 1.0 / ((steps_number + 1) * 1.5)

    while t <= 1.0:
        t3 = t ** 3
        t2 = t ** 2

        p1_mul = 2 * t3 - 3 * t2 + 1
        p4_mul = -2 * t3 + 3 * t2
        r1_mul = t3 - 2 * t2 + t
        r4_mul = t3 - t2

        x = p1x * p1_mul + p4x * p4_mul + r1x * r1_mul + r4x * r4_mul
        y = p1y * p1_mul + p4y * p4_mul + r1y * r1_mul + r4y * r4_mul

        draw_func(tools.Pixel(round(x), round(y)))

        t += t_incr