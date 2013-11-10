#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import linalg
from math import sin, cos

import tools


MOVE = 'MOVE'
ROTATE = 'ROTATE'
SCALSE = 'SCALE'
AXIS_X = 'AXIS_X'
AXIS_Y = 'AXIS_Y'
AXIS_Z = 'AXIS_Z'
POSITIVE = 'DIRECTION_POSITIVE'
NEGATIVE = 'DIRECTION_NEGATIVE'


class Transformator(object):
    def __init__(self, move_delta=1, rotate_angle=.1, scale_delta=1):
        self._move_delta = move_delta
        self._rotate_angle = rotate_angle
        self._scale_delta = scale_delta

        self._transforms = {
            MOVE: {
                POSITIVE: {
                    AXIS_X: Transform(T(move_delta, 0, 0)),
                    AXIS_Y: Transform(T(0, move_delta, 0)),
                    AXIS_Z: Transform(T(0, 0, self._move_delta)),
                },
                NEGATIVE: {
                    AXIS_X: Transform(T(-move_delta, 0, 0)),
                    AXIS_Y: Transform(T(0, -move_delta, 0)),
                    AXIS_Z: Transform(T(0, 0, -move_delta)),
                },
            },
            ROTATE: {
                POSITIVE: {
                    AXIS_X: Transform(Rx(rotate_angle)),
                    AXIS_Y: Transform(Ry(rotate_angle)),
                    AXIS_Z: Transform(Rz(rotate_angle)),
                },
                NEGATIVE: {
                    AXIS_X: Transform(Rx(-rotate_angle)),
                    AXIS_Y: Transform(Ry(-rotate_angle)),
                    AXIS_Z: Transform(Rz(-rotate_angle)),
                },
            },
        }

    def move(self, figure, direction, axis):
        transform = self._transforms[MOVE][direction][axis]
        self.apply_transform(figure, transform)

    def rotate(self, figure, direction, axis):
        rotate_transform = self._transforms[ROTATE][direction][axis]
        xc, yc, zc, wc = figure.points[0]#figure.center()
        move_to_center_matrix = T(xc, yc, zc)
        transform = Transform(linalg.inv(move_to_center_matrix) *
                              rotate_transform.matrix *
                              move_to_center_matrix)
        self.apply_transform(figure, transform)

    def apply_transform(self, figure, transform):
        for point_number, point in enumerate(figure.points):
            transformed_point = transform.transform_point(point)
            figure.set_point(transformed_point, point_number)


class Transform(object):
    def __init__(self, *matrixes):
        self._matrixes = matrixes

        self._M = self._matrixes[0]
        for matrix in self._matrixes[1:]:
            self._M *= matrix

    def transform_point(self, point):
        res = np.matrix(point) * self._M
        res /= res[0, 3]
        coodrinates = [tools.rounded_int(coord) for coord in res.tolist()[0]]
        return tools.Point(*coodrinates)

    @property
    def matrix(self):
        return self._M


def T(dx, dy, dz):
    """ Transference """
    return np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1],
    ])

def S(sx, sy, sz):
    """ Scale """
    return np.matrix([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1],
    ])

def Rx(q):
    """ Rotation around x axis"""
    sin_q, cos_q = sin(q), cos(q)
    return np.matrix([
        [1, 0, 0, 0],
        [0, cos_q, sin_q, 0],
        [0, -sin_q, cos_q, 0],
        [0, 0, 0, 1],
    ])

def Ry(q):
    """ Rotation around y axis"""
    sin_q, cos_q = sin(q), cos(q)
    return np.matrix([
        [cos_q, 0, -sin_q, 0],
        [0, 1, 0, 0],
        [sin_q, 0, cos_q, 0],
        [0, 0, 0, 1],
    ])

def Rz(q):
    """ Rotation around z axis"""
    sin_q, cos_q = sin(q), cos(q)
    return np.matrix([
        [cos_q, sin_q, 0, 0],
        [-sin_q, cos_q, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])