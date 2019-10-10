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
    Read data from a qhull format file.

    Parameters
    ----------
    filename : String with input file name.
    
    Returns
    -------
    ndim : Number of dimensions (e.g. 3 for a 3d data set).
    points : ndarray of input points.

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
    Write data to a qhull format file.

    Parameters
    ----------
    filename : String with input file name.
    points : ndarray of points.

    """
    hullfile = open(filename, 'w')
    npoints, ndim = points.shape
    
    print(ndim, file=hullfile)
    print(npoints, file=hullfile)

    for row in points:
        print(' '.join('%s' % p for p in row), file=hullfile)

    hullfile.close()

