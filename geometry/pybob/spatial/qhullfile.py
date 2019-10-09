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
    """
    readQhullFile(filename)

    Read data from a qhull format file.

    :param filename: String with input file name.
    
    :returns ndim: Number of dimensions (e.g. 3 for a 3d data set).
    :returns points: ndarray of input points.

    """

    hullfile = open(filename)
    ndim    = int(hullfile.readline())
    npoints = int(hullfile.readline())
    points = numpy.zeros((npoints,ndim))
    for npt in range(npoints):
        points[npt] = numpy.fromstring(hullfile.readline(), sep=' ')

    hullfile.close()

    return ndim, points

def writeQhullFile(filename, points):
    """
    writeQhullFile(filename, points)

    Writes data to a qhull format file.

    :param filename: String with input file name.
    :param points: ndarray of points.
    

    """
    hullfile = open(filename, 'w')
    npoints, ndim = points.shape
    
    print(ndim, file=hullfile)
    print(npoints, file=hullfile)

    for row in points:
        print(' '.join('%s' % p for p in row), file=hullfile)

    hullfile.close()

