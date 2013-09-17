#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
import collections
Point4 = collections.namedtuple('Point4', 'x y z a')

from tools import multicopy

class Point(Point4):
    def __new__(_cls, x, y, z=0, a=0):
        """
        >>> Point(2, 3)
        PlotPoint(x=2, y=3, z=0, a=0)
        """
        return Point4.__new__(_cls, x, y, z, a)

    def __repr__(self):
        return 'PlotPoint(x=%r, y=%r, z=%r, a=%r)' % self


class Plot(QObject):
    """
    >>> Plot(Point(1, 2, 3, 4))
    Plot(size_point=PlotPoint(x=1, y=2, z=3, a=4), default_value=0)
    >>> Plot(Point(2, 3, 4, 5), 'x')
    Plot(size_point=PlotPoint(x=2, y=3, z=4, a=5), default_value='x')
    """

    updated = Signal()

    def __init__(self, parent, size_point, default_value=0):
        super(Plot, self).__init__(parent)
        self._default_value = default_value
        self._size_point = size_point

        self._vector = multicopy(
            multicopy(
                multicopy(
                    multicopy(default_value,
                              size_point.a),
                    size_point.z
                ), size_point.y
            ), size_point.x
        )
        self.updated.emit()

    @property
    def size(self):
        return self._size_point

    def __getitem__(self, point):
        return self._vector[point.x][point.y][point.z][point.a]

    def __setitem__(self, point, value):
        self._vector[point.x][point.y][point.z][point.a] = value
        self.updated.emit()

    def __repr__(self):
        return "Plot(size_point=%r, default_value=%r)" % (self._size_point, self._default_value)

    def __iter__(self):
        for a in xrange(self._size_point.a):
            for z in xrange(self._size_point.z):
                for y in xrange(self._size_point.y):
                    for x in xrange(self._size_point.x):
                        yield Point(x, y, z, a)
