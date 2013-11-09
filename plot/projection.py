#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools, figure


class Projector(object):
    def __init__(self, k):
        self._k = k

    def point(self, x, y, z, w=1.0):
        return tools.Point(x, y, z + self._k, w)

    def project_point(self, point):
        x0, y0, z0, w0 = point
        x = self._k * x0 / z0
        y = self._k * y0 / z0
        return tools.Pixel(x, y)

    def project_line(self, line):
        return figure.Line([
            self.project_point(line.pixels[0]),
            self.project_point(line.pixels[1]),
        ])
