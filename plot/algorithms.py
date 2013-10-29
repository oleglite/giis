#!/usr/bin/env python
# -*- coding: utf-8 -*-
from plot import figure

import tools
import collections
import reflections

by_name = collections.OrderedDict()


def algorithm(name, figure_cls, alpha=False):
    def wrap(func):
        func.NAME = name
        func.Figure = figure_cls
        func.alpha = alpha
        by_name[name] = func
        return func
    return wrap


@algorithm(name=u'ЦДА', figure_cls=figure.Line)
def DDA(figure):
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
        yield tools.rounded_int(x), tools.rounded_int(y)
        x += dx
        y += dy


@algorithm(name=u'Алгоритм Брезенхема', figure_cls=figure.Line)
def bresenham(figure):
    point1, point2 = figure.points
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1

    error = dx - dy
    while x1 != x2 or y1 != y2:
        yield x1, y1
        error2 = error * 2
        if error2 > -dy:
            error -= dy
            x1 += signX
        if error2 < dx:
            error += dx
            y1 += signY
    yield x2, y2

@algorithm(name=u'Алгоритм Ву', figure_cls=figure.Line, alpha=True)
def wu(figure):
    point1, point2 = figure.points
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    signX = 1 if x1 < x2 else -1
    signY = 1 if y1 < y2 else -1

    if not dx:
        for y in xrange(y1, y2 + signY, signY):
            yield x1, y
        return

    if not dy:
        for x in xrange(x1, x2 + signX, signX):
            yield x, y1
    gradientY = float(dy) / dx
    gradientX = float(dx) / dy

    if dx > dy:
        for x in xrange(x1, x2 + signX, signX):
            y = y1 + abs(x - x1) * gradientY * signY
            y_pos = tools.fpart(y)
            yield x, int(y), (1 - y_pos)
            yield x, int(y) + 1, y_pos
    else:
        for y in xrange(y1, y2 + signY, signY):
            x = x1 + abs(y - y1) * gradientX * signX
            x_pos = tools.fpart(x)
            yield int(x), y, (1 - x_pos)
            yield int(x) + 1, y, x_pos

@algorithm(name=u'Алгоритм Брезенхема для окружности', figure_cls=figure.Circle)
def bresenham_circle(circle):
    reflector = reflections.Reflector()
    h_line = figure.Line([circle.points[0], tools.Pixel(circle.x0 + circle.R, circle.y0)])
    reflector.add_reflection(reflections.LineReflection(h_line))
    reflector.add_reflection(reflections.PointReflection(circle.points[0]))

    x, y = 0, circle.R
    di = 0

    while y >= 0:
        for point in reflector.reflect(x + circle.x0, int(y) + circle.y0):
            yield point

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
def bres_like_parabola(parabola):
    x1, y1 = parabola.points[0]
    x2, y2 = parabola.points[1]

    p = abs(x1 - x2)
    increment = tools.sign(x1 - x2)

    x = x1 - increment * p / 2
    y0 = y1
    y = 0

    x_max = parabola.params['scene_size'].width

    di = 0

    yield x, y0

    if not p:
        return

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

        yield x, y0 + y
        yield x, y0 - y

def count_steps(points):
    return tools.max_diff([point.x for point in points]) + tools.max_diff([point.y for point in points])

@algorithm(u'Метод Эрмита', figure.Curve)
def ermit_curve(curve):
    p1x, p1y = curve.points[0]
    p4x, p4y = curve.points[1]
    r1x, r1y = curve.points[2]
    r4x, r4y = curve.points[3]

    r1x -= p1x
    r1y -= p1y
    r4x -= p4x
    r4y -= p4y

    t = 0.0
    steps_number = count_steps(curve.points)
    t_incr = 1.0 / (steps_number + 1)

    while t <= 1.0:
        t3 = t ** 3
        t2 = t ** 2

        p1_mul = 2 * t3 - 3 * t2 + 1
        p4_mul = -2 * t3 + 3 * t2
        r1_mul = t3 - 2 * t2 + t
        r4_mul = t3 - t2

        x = p1x * p1_mul + p4x * p4_mul + r1x * r1_mul + r4x * r4_mul
        y = p1y * p1_mul + p4y * p4_mul + r1y * r1_mul + r4y * r4_mul

        yield tools.rounded_int(x), tools.rounded_int(y)

        t += t_incr

@algorithm(u'Кривая Безье', figure.Curve)
def bezier_curve(curve):
    p1x, p1y = curve.points[0]
    p4x, p4y = curve.points[1]
    p2x, p2y = curve.points[2]
    p3x, p3y = curve.points[3]

    t = 0.0
    steps_number = count_steps(curve.points)
    t_incr = 1.0 / ((steps_number + 1) * 2)

    while t <= 1.0:
        p1_mul = (1 - t) ** 3
        p2_mul = 3 * t * ((t - 1) ** 2)
        p3_mul = 3 * (t ** 2) * (1 - t)
        p4_mul = t ** 3

        x = p1x * p1_mul + p2x * p2_mul + p3x * p3_mul + p4x * p4_mul
        y = p1y * p1_mul + p2y * p2_mul + p3y * p3_mul + p4y * p4_mul

        yield tools.rounded_int(x), tools.rounded_int(y)

        t += t_incr


@algorithm(u'B-сплайн', figure.ExtendibleCurve)
def b_splain(curve):
    for p0, p1, p2, p3 in tools.ntuples(curve.points, 4):
        a0, a1, a2, a3 = b_splain_coefs(p0.x, p1.x, p2.x, p3.x)
        b0, b1, b2, b3 = b_splain_coefs(p0.y, p1.y, p2.y, p3.y)

        steps_number = count_steps([p0, p1, p2, p3])
        t_incr = 1.0 / (steps_number + 1)

        t = 0.0
        while t <= 1.0:
            x = ((a3 * t + a2) * t + a1) * t + a0
            y = ((b3 * t + b2) * t + b1) * t + b0

            yield tools.rounded_int(x), tools.rounded_int(y)

            t += t_incr

def b_splain_coefs(v0, v1, v2, v3):
    c3 = (-v0 + 3 * v1 - 3 * v2 + v3) / 6.
    c2 = (v0 - 2 * v1 + v2) / 2.
    c1 = (-v0 + v2) / 2.
    c0 = (v0 + 4 * v1 + v2) / 6.
    return c0, c1, c2, c3

