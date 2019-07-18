# spatial
Some variations and samples on the scipy.spatial theme

Note: All of this was built on a debian stable distribution using the
latest version of python3.x that comes with the distro.  In many cases
I had to upgrade packages to more recent versions using pip3.  Some of
the code requires some modifications I made (with lots of help from
Tyler Reddy) to scipy.spatial.  None of this has been tested on a
Windows machine.  I don't think this even works with python2.x.

Programs and data in this repository.

-- qhulldata: Directory containing some data files in qhull format.  These can
   be used directly with qhull and most of the programs will read qhull files.
  
    visible*: Data files in the qhull format for playing with visible facets.
    spheredata*: Data files in the qhull format for playing with visible facets
                 or spherical geometry structures.

-- appendzero.py: Program to take a qhull file and append a row of zeros.

-- 2dvisible.py

  Program to experiment with visible facets in 2d.  Lots of graphics and interactions.

-- 3dvisible.py

  Program to experiment with visible facets in 3d (nd actually).  Just reads a file
  and prints the results.  No graphics.

