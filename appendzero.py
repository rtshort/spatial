#!/usr/bin/python3

"""
Takes a qhull file on the standard input, prepends the origin and
writes the modified file to the stdout in qhull format.
"""
#
# Copyright (C)  Robert T. Short, 2019.
#
# Distributed under the same BSD license as Scipy.
#


import sys
import numpy

ndim    = int(sys.stdin.readline())
npoints = int(sys.stdin.readline())
points = numpy.zeros((npoints,ndim))
for npt in range(npoints):
    points[npt] = numpy.fromstring(sys.stdin.readline(), sep=' ')

points = numpy.vstack((points, numpy.zeros(ndim)))

print(ndim)
print(npoints+1)

for row in points:
    print(' '.join('%s' % p for p in row))
