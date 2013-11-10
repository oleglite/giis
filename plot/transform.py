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

transform_shortcuts = dict(
    ROTATE_X_POS = (ROTATE, POSITIVE, AXIS_X),
    ROTATE_X_NEG = (ROTATE, NEGATIVE, AXIS_X),
    ROTATE_Y_POS = (ROTATE, POSITIVE, AXIS_Y),
    ROTATE_Y_NEG = (ROTATE, NEGATIVE, AXIS_Y),
    ROTATE_Z_POS = (ROTATE, POSITIVE, AXIS_Z),
    ROTATE_Z_NEG = (ROTATE, NEGATIVE, AXIS_Z),

    MOVE_X_POS = (MOVE, POSITIVE, AXIS_X),
    MOVE_X_NEG = (MOVE, NEGATIVE, AXIS_X),
    MOVE_Y_POS = (MOVE, POSITIVE, AXIS_Y),
    MOVE_Y_NEG = (MOVE, NEGATIVE, AXIS_Y),
    MOVE_Z_POS = (MOVE, POSITIVE, AXIS_Z),
    MOVE_Z_NEG = (MOVE, NEGATIVE, AXIS_Z),

    SCALE_X_POS = (SCALSE, POSITIVE, AXIS_X),
    SCALE_X_NEG = (SCALSE, NEGATIVE, AXIS_X),
    SCALE_Y_POS = (SCALSE, POSITIVE, AXIS_Y),
    SCALE_Y_NEG = (SCALSE, NEGATIVE, AXIS_Y),
    SCALE_Z_POS = (SCALSE, POSITIVE, AXIS_Z),
    SCALE_Z_NEG = (SCALSE, NEGATIVE, AXIS_Z),
)


class FigureTransformator(object):
    def __init__(self, move_delta=1, rotate_angle=.1, scale_factor=1.2):
        self._move_delta = move_delta
        self._rotate_angle = rotate_angle
        self._scale_delta = scale_factor

        self._transforms = {
            MOVE: {
                POSITIVE: {
                    AXIS_X: T(move_delta, 0, 0),
                    AXIS_Y: T(0, move_delta, 0),
                    AXIS_Z: T(0, 0, self._move_delta),
                },
                NEGATIVE: {
                    AXIS_X: T(-move_delta, 0, 0),
                    AXIS_Y: T(0, -move_delta, 0),
                    AXIS_Z: T(0, 0, -move_delta),
                },
            },
            ROTATE: {
                POSITIVE: {
                    AXIS_X: Rx(rotate_angle),
                    AXIS_Y: Ry(rotate_angle),
                    AXIS_Z: Rz(rotate_angle),
                },
                NEGATIVE: {
                    AXIS_X: Rx(-rotate_angle),
                    AXIS_Y: Ry(-rotate_angle),
                    AXIS_Z: Rz(-rotate_angle),
                },
            },
            SCALSE: {
                POSITIVE: {
                    AXIS_X: S(scale_factor, 1, 1),
                    AXIS_Y: S(1, scale_factor, 1),
                    AXIS_Z: S(1, 1, scale_factor),
                },
                NEGATIVE: {
                    AXIS_X: S(1 / scale_factor, 1, 1),
                    AXIS_Y: S(1, 1 / scale_factor, 1),
                    AXIS_Z: S(1, 1, 1 / scale_factor),
                },
            }
        }

    def transform(self, figure, shortcut):
        transform, direction, axis = transform_shortcuts[shortcut]
        transform_matrix = self._transforms[transform][direction][axis]

        if transform == MOVE:
            figure.apply_matrix(transform_matrix)
        else:
            self.__from_center(figure, transform_matrix)

    def __from_center(self, figure, transform_matrix):
        xc, yc, zc, wc = figure.center()
        move_to_center_matrix = T(xc, yc, zc)
        figure.apply_matrix(linalg.inv(move_to_center_matrix))
        figure.apply_matrix(transform_matrix)
        figure.apply_matrix(move_to_center_matrix)


class Transform(object):
    def __init__(self, *matrixes):
        self._M = np.matrix(np.identity(4))
        for matrix in matrixes:
            self._M *= matrix

    def apply_matrix(self, matrix):
        self._M *= matrix

    def transform_point(self, point):
        res = np.matrix(point) * self._M
        res /= res[0, 3]
        coodrinates = [tools.rounded_int(coord) for coord in res.tolist()[0]]
        return tools.Point(*coodrinates)


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