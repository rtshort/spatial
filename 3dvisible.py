import numpy

from scipy.spatial import ConvexHull
from qhullfile import readQhullFile

# Read the qhull file.

filename = 'qhulldata/spheredata2'
#filename = 'jcircledata1'

ndim,points  = readQhullFile(filename)
npoints = len(points)

points  = numpy.vstack((points,numpy.zeros(ndim)))

print(ndim,npoints)
print(points)

# Compute the visible and invisible facets.

qhull_options = "QG-"+str(npoints)
hull = ConvexHull(points, qhull_options=qhull_options)

print('Not visible from the origin')
print(hull.good)
print(hull.points)
print(hull.simplices)

qhull_options = "QG"+str(npoints)
hull = ConvexHull(points, qhull_options=qhull_options)

print('Visible from the origin')
print(hull.good)
print(hull.points)
print(hull.simplices)

print('Visible\n', hull.simplices[hull.good])
print('Not visible\n', hull.simplices[~hull.good])

