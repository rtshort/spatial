#!/usr/bin/python3

"""

Takes a 2d qhull file on the standard input, appends the origin and
writes the modified file to the standard output in qhull format.  This
is mostly for experimenting with visible facets.  See the qhull
documentation for the qhull file format.

Example
=======
From the command line:

> cat qhulldata/visible1 | ./appendzero.py
2
8
2.8357815 1.91145534
2.55940908 2.69475804
1.35189884 2.95484612
1.02629326 2.23106931
1.35493431 1.21118976
2.28381929 1.26192649
2.09812 1.80199967
0.0 0.0
> cat qhulldata/visible1 | ./appendzero.py | qhull i QG0 Qt
3
3 4 
2 3 
4 5 
> cat qhulldata/visible1 | ./appendzero.py | qhull i QG-0 Qt
3
5 0 
0 1 
1 2

"""
#
# Copyright (C)  Robert T. Short, 2019.
#
# Distributed under the same BSD license as Scipy.
#


import sys
import numpy

if __name__ == "__main__":

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
