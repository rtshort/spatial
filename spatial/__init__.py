"""
spatial
======= 

This package contains some variations and samples on the scipy.spatial
theme.  All of the programs provided here should work right out of the
box, but most of them will take a little effort to understand.  They
are all noisy in the sense that interacting with the plot windows will
print a lot of data to the standard output.

Note: All of this was built on a debian stable distribution using the
latest version of python3.x that comes with the distro.  In many cases
I had to upgrade packages to more recent versions using pip3,
especially numpy.  None of this has been tested on a Windows machine.
I don't think this even works with python2.x.

Some of the code requires some modifications I made (with lots of help
from Tyler Reddy) to scipy.spatial.  When scipy 1.4.0 is released
those modifications will be generally available, but until then you
will have to build scipy from the github sources.

.. toctree::
   :maxdepth: 1

   appendzero
   visible2d
   visible3d
   qhulldata

"""
import spatial.appendzero
import spatial.visible2d
import spatial.visible3d
import spatial.qhulldata
