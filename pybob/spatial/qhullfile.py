"""
Utilities to read and write qhull files.

"""
#
# Copyright (C)  Robert T. Short, 2019.
#
# Distributed under the same BSD license as Scipy.
#

import numpy

def readQhullFile(filename):

    hullfile = open(filename)
    ndim    = int(hullfile.readline())
    npoints = int(hullfile.readline())
    points = numpy.zeros((npoints,ndim))
    for npt in range(npoints):
        points[npt] = numpy.fromstring(hullfile.readline(), sep=' ')

    hullfile.close()

    return ndim, points

def writeQhullFile(filename, points):

    hullfile = open(filename, 'w')
    npoints, ndim = points.shape
    
    print(ndim, file=hullfile)
    print(npoints, file=hullfile)

    for row in points:
        print(' '.join('%s' % p for p in row), file=hullfile)

    hullfile.close()

