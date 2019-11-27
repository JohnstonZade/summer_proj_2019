# -- IMPORTS -- #

# -- for testing on laptop -- #
import sys
sys.path.insert(1, '/home/zade/athena/vis/python')
# -- for testing on laptop -- #

# use numpy?

# TODO: Write up code for this. Start with 2D case and use 2D slices from sim.
# TODO: Install hdf5 and fft and use hard drive for files
# TODO: .local-7.3 get from drive and update .bashrc
# TODO: set up github

# get grid sizes (i.e Lx Ly Lz)
# 2D case first
# get N_p pairs of random points on the grid
# be careful with python 0-index and compare to data file.
# i.e. (L1x, L1y) = randint(N_p, Lx), randint(N_p, Ly)
#      (L2x, L2y) = randint(N_p, Lx), randint(N_p, Ly)

# get actual position vector components for each pair of grid points
# find distance between each pair of points; this is l
# be careful with periodicity but not important at first
# try plotting a histogram of l to see distribution

# for each pair of position vectors x1, x2 say
# get velocity vectors u1, u2 at each point
# calculate Δu2 = abs(u1 - u2)**2
# we now have a mapping of l to Δu2! <- structure function!

# create an l-grid (l_min to l_max in N_l steps?)
# for l_i and l_i+1 in grid
# use where(l_i < l < l_i+1) for get logical array
# use this to find Δu2 in this range and average over all.
# bin at (l_i + l_i+1)/2 (otherwise we have N_l-1 y values but N_l x values)
# should see l^(-2/3)?
