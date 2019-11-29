'''Code to calculate structure function of a fluid simulation.
Not sure if it works on Thunderbird as it seems to be running
Python 2.
'''
# Change to athena_read dir
import sys; sys.path.insert(1, '/home/zade/athena/vis/python')
from athena_read import athdf
from numpy import array, linspace, logical_and, mean, meshgrid, sqrt, sum
from numpy import where, zeros
from numpy.random import randint
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)  # LaTeX labels


def get_mag(X1, X2):
    '''Returns the magnitude of the difference of given vectors.'''
    x1, x2 = array(X1), array(X2)
    return sqrt(sum((x2-x1)**2, axis=1))


# Check todos
def structure_function(fname, do_ldist=0):
    '''Calculates and plots structure function
    assuming isotropy of turbulence.

    Takes in file name and boolean for plotting distribution of lengths.
    '''
    def get_mean(i):
        '''Selects and averages the difference in velocity values squared at
        between two points with distance l between them.
        Selection depends on whether l_grid[i] <= l < l_grid[i+1].
        '''
        l_logic = where(logical_and(l_grid[i] <= l_vec, l_vec < l_grid[i+1]))

        # Stops error for mean of empty slice
        # Might be a better way to handle this
        if len(Δu2[l_logic]) == 0:
            return float('nan')

        return mean(Δu2[l_logic])

    def get_length():
        '''Returns the dimensions of the simulation.'''
        names = ['RootGridX3', 'RootGridX2', 'RootGridX1']
        return array([data[name][1]-data[name][0] for name in names])

    def get_vel(p):
        '''Returns the velocity vector at a given point.'''
        tp = tuple(p)
        v1 = vel_data[0][tp]  # x-component
        v2 = vel_data[1][tp]  # y-component
        v3 = vel_data[2][tp]  # z-component
        return array([v1, v2, v3])

    def get_point(p):
        '''Returns coordinate of given grid point.'''
        tp = tuple(p)
        return array([zz[tp], yy[tp], xx[tp]])

    # Read in data and set up grid
    # TODO: use fname parameter
    filename = '/media/zade/Seagate Expansion Drive/Summer_Project_2019/'
    filename += 'hydro_cont_turb_128/Turb.out2.00001.athdf'
    data = athdf(filename)

    # Following (z, y, x) convention from athena_read
    grid = data['RootGridSize'][::-1]
    zz, yy, xx = meshgrid(data['x3f'], data['x2f'], data['x1f'], indexing='ij')
    # t = data['Time']

    # Get N_p pairs of random points on the grid
    # Assuming turbulence is isotropic
    # TODO:
    # Am I wanting to average over all time or make a time evolution?
    # Do I need to randomize points for each file?
    N_p = int(1e6)
    L1 = randint(0, grid, size=(N_p, len(grid)))
    L2 = randint(0, grid, size=(N_p, len(grid)))
    print("Points generated")

    # Get actual position vector components for each pair of grid points
    x1_vec = array([get_point(p) for p in L1])
    x2_vec = array([get_point(p) for p in L2])

    # Find distance between each pair of points
    # Why do I need to be careful with periodicity?
    l_vec = get_mag(x1_vec, x2_vec)
    print('Distances calculated')

    # Check distribution of l's
    if do_ldist:
        n, bins, patches = plt.hist(l_vec, 100)
        plt.title(r'Distribution of $L$')
        plt.xlabel('Distance between points')
        plt.ylabel('Counts')
        plt.show()

    # For each pair of position vectors x1, x2
    # Get velocity vectors u1, u2 at each point
    # Calculate Δu2 = abs(u1 - u2)**2
    # We now have a mapping of l to Δu2! <- structure function!
    vel_data = (data['vel1'], data['vel2'], data['vel3'])
    u1_vec = array([get_vel(p) for p in L1])
    u2_vec = array([get_vel(p) for p in L2])
    Δu2 = get_mag(u1_vec, u2_vec)
    print('Velocities calculated')

    # Bin and plot structure function
    N_l = 100
    l_grid = linspace(min(l_vec), max(l_vec), N_l)
    Δu_avg = zeros(N_l-1, float)
    l_axis = zeros(N_l-1, float)

    for i in range(N_l-1):
        Δu_avg[i] = get_mean(i)
        l_axis[i] = 0.5*(l_grid[i]+l_grid[i+1])

    # TODO: Am I meant to be using histogram?
    plt.plot(l_axis, Δu_avg)
    plt.title(r'$S_2(l)$')
    plt.xlabel(r'$l$')
    plt.ylabel('Structure Function')
    plt.show()


structure_function('', 1)
