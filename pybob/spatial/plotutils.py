#
#  This is just the _2d plotting collection from scipy.spatial, but
#  I fixed it so furthest site diagrams work, modified some scaling things
#  and added a routine to return a list of polygons that represent the
#  Voronoi regions.
#
#  R.T. Short, 12/2018.

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy import arctan2

from scipy._lib.decorator import decorator as _decorator

__all__ = ['delaunay_plot_2d', 'convex_hull_plot_2d', 'voronoi_plot_2d']


@_decorator
def _held_figure(func, obj, ax=None, **kw):
    import matplotlib.pyplot as plt

    if ax is None:
        fig = plt.figure()
        ax = fig.gca()
        return func(obj, ax=ax, **kw)
    else:
        return func(obj, ax=ax, **kw)

def _adjust_bounds(ax, points):
    margin = 0.1 * points.ptp(axis=0)
    xy_min = points.min(axis=0) - margin
    xy_max = points.max(axis=0) + margin
    ax.set_xlim(xy_min[0], xy_max[0])
    ax.set_ylim(xy_min[1], xy_max[1])


@_held_figure
def delaunay_plot_2d(tri, ax=None):
    """
    Plot the given Delaunay triangulation in 2-D

    Parameters
    ----------
    tri : scipy.spatial.Delaunay instance
        Triangulation to plot
    ax : matplotlib.axes.Axes instance, optional
        Axes to plot on

    Returns
    -------
    fig : matplotlib.figure.Figure instance
        Figure for the plot

    See Also
    --------
    Delaunay
    matplotlib.pyplot.triplot

    Notes
    -----
    Requires Matplotlib.

    Examples
    --------

    >>> import matplotlib.pyplot as plt
    >>> from scipy.spatial import Delaunay, delaunay_plot_2d

    The Delaunay triangulation of a set of random points:

    >>> points = np.random.rand(30, 2)
    >>> tri = Delaunay(points)

    Plot it:

    >>> _ = delaunay_plot_2d(tri)
    >>> plt.show()

    """
    if tri.points.shape[1] != 2:
        raise ValueError("Delaunay triangulation is not 2-D")

    x, y = tri.points.T
    ax.scatter(x, y)
    ax.triplot(x, y, tri.simplices.copy())

    _adjust_bounds(ax, tri.points)

    return ax.figure


@_held_figure
def convex_hull_plot_2d(hull, ax=None):
    """
    Plot the given convex hull diagram in 2-D

    Parameters
    ----------
    hull : scipy.spatial.ConvexHull instance
        Convex hull to plot
    ax : matplotlib.axes.Axes instance, optional
        Axes to plot on

    Returns
    -------
    fig : matplotlib.figure.Figure instance
        Figure for the plot

    See Also
    --------
    ConvexHull

    Notes
    -----
    Requires Matplotlib.


    Examples
    --------

    >>> import matplotlib.pyplot as plt
    >>> from scipy.spatial import ConvexHull, convex_hull_plot_2d

    The convex hull of a random set of points:

    >>> points = np.random.rand(30, 2)
    >>> hull = ConvexHull(points)

    Plot it:

    >>> _ = convex_hull_plot_2d(hull)
    >>> plt.show()

    """
    from matplotlib.collections import LineCollection

    if hull.points.shape[1] != 2:
        raise ValueError("Convex hull is not 2-D")

    ax.scatter(hull.points[:,0], hull.points[:,1], marker='o', color='green')
    line_segments = [hull.points[simplex] for simplex in hull.simplices]
    ax.add_collection(LineCollection(line_segments,
                                     colors='k',
                                     linestyle='solid',
                                     alpha=0.5))
    _adjust_bounds(ax, hull.points)

    return ax.figure


def infiniteRidge(vor, center,  ptp_bound, pointidx, simplex, furthest_site):

    i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

    t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
    t /= np.linalg.norm(t)
    n = np.array([-t[1], t[0]])  # normal

    midpoint = vor.points[pointidx].mean(axis=0)
    direction = np.sign(np.dot(midpoint - center, n)) * n
    if (furthest_site):
        direction = -direction
    far_point = vor.vertices[i] + direction * 2*ptp_bound.max()

    return np.stack((vor.vertices[i], far_point))

    

@_held_figure
def voronoi_plot_2d(vor, ax=None, **kw):
    """
    Plot the given Voronoi diagram in 2-D

    Parameters
    ----------
    vor : scipy.spatial.Voronoi instance
        Diagram to plot
    ax : matplotlib.axes.Axes instance, optional
        Axes to plot on
    show_points: bool, optional
        Add the Voronoi points to the plot.
    show_vertices : bool, optional
        Add the Voronoi vertices to the plot.
    line_colors : string, optional
        Specifies the line color for polygon boundaries
    line_width : float, optional
        Specifies the line width for polygon boundaries
    line_alpha: float, optional
        Specifies the line alpha for polygon boundaries
    point_size: float, optional
        Specifies the size of points


    Returns
    -------
    fig : matplotlib.figure.Figure instance
        Figure for the plot

    See Also
    --------
    Voronoi

    Notes
    -----
    Requires Matplotlib.

    Examples
    --------
    Set of point:

    >>> import matplotlib.pyplot as plt
    >>> points = np.random.rand(10,2) #random

    Voronoi diagram of the points:

    >>> from scipy.spatial import Voronoi, voronoi_plot_2d
    >>> vor = Voronoi(points)

    using `voronoi_plot_2d` for visualisation:

    >>> fig = voronoi_plot_2d(vor)

    using `voronoi_plot_2d` for visualisation with enhancements:

    >>> fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange',
    ...                 line_width=2, line_alpha=0.6, point_size=2)
    >>> plt.show()

    """
    from matplotlib.collections import LineCollection

    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    if kw.get('show_points', True):
        point_size = kw.get('point_size', None)
        ax.plot(vor.points[:,0], vor.points[:,1], '.', markersize=point_size)
    if kw.get('show_vertices', True):
        ax.scatter(vor.vertices[:,0], vor.vertices[:,1], color='orange', marker='o')

    furthest_site = vor.furthest_site

    center = vor.points.mean(axis=0)
    ptp_bound = vor.points.ptp(axis=0)

    line_colors = kw.get('line_colors', 'k')
    line_width = kw.get('line_width', 1.0)
    line_alpha = kw.get('line_alpha', 1.0)

    finite_segments = []
    infinite_segments = []
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            finite_segments.append(vor.vertices[simplex])
        else:
            vertex = infiniteRidge(vor, center, ptp_bound, pointidx, simplex, furthest_site)
            infinite_segments.append(vertex)

    #print('finite_segments\n', finite_segments)
    #print('infinite_segments\n', infinite_segments)
    ax.add_collection(LineCollection(finite_segments,
                                     colors=line_colors,
                                     lw=line_width,
                                     alpha=line_alpha,
                                     linestyle='solid'))
    ax.add_collection(LineCollection(infinite_segments,
                                     colors=line_colors,
                                     lw=line_width,
                                     alpha=line_alpha,
                                     linestyle='dashed'))

    _adjust_bounds(ax, np.vstack((vor.points,vor.vertices)))

    return ax.figure

def getVoronoiRegions(vor):
    """

    Get a list of polygons representing the Voronoi regions in a planar (2d) Voronoi diagram. 

    Parameters
    ----------
    vor : scipy.spatial.Voronoi instance.
    furthest_site: True for a furthest site diagram, false otherwise.

    Returns
    -------
    voronoi_polygons: A set of polygons, each representing a Voronoi region.  

    See Also
    --------
    Voronoi


    Examples
    --------

    >>> import numpy
    >>> from scipy.spatial import Voronoi
    >>> from plotutils import voronoi_plot_2d, getVoronoiRegions
    >>> import matplotlib.pyplot as plt
    >>> from matplotlib.patches import Polygon

    Generate some points.  This is a quasi-rectangular region in the plane.

    >>> points = numpy.array([[ 0.87768882, -0.02146875 ],
    >>>                       [-0.20462553,  1.09510478 ],
    >>>                       [-0.88256750,  0.18082183 ],
    >>>                       [-0.17671794, -0.94754607 ]])

    Generate a nearest site Voronoi tesselation from the points.

    >>> vor = Voronoi(points)

    Create a figure and plot the Voronoi diagram.

    >>> fig1 = plt.figure('Voronoi (nearest site)')
    >>> ax1  = fig1.add_subplot(111)

    >>> voronoi_plot_2d(vor, ax=ax1, show_points=True)

    Now get the polygons that make up the Voronoi regions.  Create
    a plottable polygon from the Voronoi region around point 0 and
    add it to the plot.  The region will be in a partially transparent
    light green.

    >>> polygons = getVoronoiRegions(vor)
    >>> region   = Polygon(polygons[0], alpha=0.2, color='lightgreen')
    >>> ax1.add_artist(region)

    Now do the same thing, but for a furthest site diagram.

    >>> vor = Voronoi(points,furthest_site=True)
    >>> fig2 = plt.figure('Voronoi (furthest site)')
    >>> ax2  = fig2.add_subplot(111)
    >>> voronoi_plot_2d(vor, ax=ax2, show_points=True, furthest_site=True)
    >>> polygons = getVoronoiRegions(vor, furthest_site=True)
    >>> region   = Polygon(polygons[0], alpha=0.2, color='lightgreen')
    >>> ax2.add_artist(region)

    Show both plots.

    >>> plt.show()

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    furthest_site = vor.furthest_site

    center = vor.points.mean(axis=0)
    ptp_bound = vor.points.ptp(axis=0)

    voronoi_polygons = []
    #print('--------- getVoronoiRegions ------')
    for pointidx in range(len(vor.points)):
        point = vor.point_region[pointidx]
        this_polygon = []
        region = vor.regions[point]
        #print('region', region)
        for idx in range(len(region)):
            vertex = region[idx]
            if (vertex>=0):
                this_polygon.append(vor.vertices[vertex])
                #print('finite ridge', vertex)
            else:
                ridge_points = []
                last = (idx-1) % len(region)
                next = (idx+1) % len(region)
                ridgelast = np.array([vertex, region[last]])
                rdx1 = [rdx for rdx in range(len(vor.ridge_vertices))
                        if all(vor.ridge_vertices[rdx]==ridgelast)]
                rdxlast = [rdx for rdx in rdx1 if any(vor.ridge_points[rdx]==pointidx)]
                for rdx in rdxlast:
                    if not(rdx in ridge_points):
                        ridge_points.append(rdx)

                ridgenext = np.array([vertex, region[next]])
                rdx2 = [rdx for rdx in range(len(vor.ridge_vertices))
                        if all(vor.ridge_vertices[rdx]==ridgenext)]
                rdxnext = [rdx for rdx in rdx2 if any(vor.ridge_points[rdx]==pointidx)]
                for rdx in rdxnext:
                    if not(rdx in ridge_points):
                        ridge_points.append(rdx)
                #print('infinite ridge', ridgelast, rdx1, rdxlast)
                #print('infinite ridge', ridgenext, rdx2, rdxnext)
                #print('infinite ridge', ridge_points)
                for ridgeidx in ridge_points:
                    infinite_vertex = infiniteRidge(vor, center, ptp_bound,
                                                    vor.ridge_points[ridgeidx],
                                                    np.asarray(vor.ridge_vertices[ridgeidx]),
                                                    furthest_site)[1]
                    #print('infinite vertex', infinite_vertex)
                    this_polygon.append(infinite_vertex)
        
        if (len(this_polygon)>0):
            this_polygon = np.vstack(this_polygon)
        voronoi_polygons.append(np.array(this_polygon))

        #print('this_polygon\n', this_polygon)

    #print('======\n', voronoi_polygons)

    return voronoi_polygons

def voronoi_plot_sphere(vor, ax=None, **kw):
    """
    Plot the given spherical Voronoi diagram

    Parameters
    ----------
    vor : SphericalVoronoi instance
        Diagram to plot
    ax : matplotlib.axes.Axes instance, optional
        Axes to plot on
    show_sphere: bool, optional
        Show the sphere.
    show_points: bool, optional
        Add the generator points (sites) to the plot.
    point_size: float, optional
        Specifies the size of generator points
    show_vertices : bool, optional
        Add the Voronoi vertices to the plot.
    line_colors : string, optional
        Specifies the line color for Voronoi region boundaries
    line_width : float, optional
        Specifies the line width for Voronoi region boundaries
    line_alpha: float, optional
        Specifies the line alpha for Voronoi region boundaries
    show_vertices : bool, optional
        Add the Voronoi vertices to the plot.
    vertex_size: float, optional
        Size of vertex points
    vertex_color: string, optional
        Color of vertex points

    Returns
    -------
    fig : matplotlib.figure.Figure instance
        Figure for the plot

    See Also
    --------
    Voronoi

    Notes
    -----
    Requires Matplotlib.

    Examples
    --------


    """

    from numpy import pi, sin, cos

    import matplotlib.pyplot as plt

    if vor.points.shape[1] != 3:
        raise ValueError("Voronoi diagram is not 3-D")

    furthest_site = vor.furthest_site

    if (ax is None):
        fig = plt.figure('Spherical Voronoi')
        ax  = fig.add_subplot(111, projection='3d')

    if kw.get('show_sphere', True):
        u = np.linspace(0, 2*pi, 100)
        v = np.linspace(0, pi, 100)
        x = np.outer(cos(u), sin(v))
        y = np.outer(sin(u), sin(v))
        z = np.outer(np.ones(np.size(u)), cos(v))

        ax.plot_surface(x, y, z, color='yellow', alpha=0.1)

    if kw.get('show_points', True):
        point_size = kw.get('point_size', None)
        ax.scatter(vor.points[:,0], vor.points[:,1], vor.points[:,2], color='blue', marker='.')

    line_colors = kw.get('line_colors', 'black')
    line_width  = kw.get('line_width', 1.0)
    line_alpha  = kw.get('line_alpha', 0.4)

    lmbda = np.linspace(0, 1, 1000)
    for rv,cnt in zip(vor.ridge_vertices,range(len(vor.ridge_vertices))):
        pts = vor.vertices[rv]
        p = np.outer(lmbda,pts[0]) + np.outer((1-lmbda),pts[1])
        p = p.T/np.linalg.norm(p,axis=1)
        ax.plot(p[0], p[1], p[2], color=line_colors, alpha=line_alpha)

    if kw.get('show_vertices', True):
        vertex_size = kw.get('vertex_size', 25.0)
        vertex_color = kw.get('vertex_color', 'orange')
        ax.scatter(vor.vertices[:,0], vor.vertices[:,1], vor.vertices[:,2],
                   color=vertex_color, marker='o',s=vertex_size)

    return ax.figure

