# spatial
Some variations and samples on the scipy.spatial theme

Note:  none of this has been tested on a Windows machine.  I don't think this even
works with python2.

Programs and data in this repository.

- visible*: Data files in the qhull format for playing with visible facets.
- spheredata*: Data files in the qhull format for playing with visible facets.

- appendzero.py: Program to take a qhull file and append a row of zeros.

For example, from the command line:

> cat visible1 | ./appendzero.py
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
> cat visible1 | ./appendzero.py | qhull i QG0 Qt
3
3 4 
2 3 
4 5 
> cat visible1 | ./appendzero.py | qhull i QG-0 Qt
3
5 0 
0 1 
1 2 

-- 2dvisible.py

  Program to experiment with visible facets in 2d.  Lots of graphics and interactions.

-- 3dvisible.py

  Program to experiment with visible facets in 3d (nd actuall).  Just reads a file
  and prints the results.

