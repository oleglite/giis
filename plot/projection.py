#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import figure


class Projector(object):
    def __init__(self, projection_point):
        self._projection_point = projection_point

    def project_point(self, point):
        xp, yp, zp, wp = self._projection_point
        x0, y0, z0, w0 = point
        x = xp + (x0 - xp) * zp / (z0 + zp)
        y = yp + (y0 - yp) * zp / (z0 + zp)
        return tools.Pixel(x, y)

    def project_line(self, line):
        return figure.Line([
            self.project_point(line.pixels[0]),
            self.project_point(line.pixels[1]),
        ])
