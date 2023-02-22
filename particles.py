import numpy as np
from scipy import spatial as sp
import pandas as pd

class Particles:
    def __init__(self, xsize, ysize):
        self.particles = pd.DataFrame(columns=['n', 'r', 'px', 'py', 'vx', 'vy'])
        self.xlim = xsize/2
        self.ylim = ysize/2

    def add_particle(self, tag, r):
        # separate x and y coordinates
        #   doubles # of matrix operations
        #   BUT makes it more ergonomic to check neighbors &tc.
        new_particle = {'n': tag, 'r': r, 'px': -3.9, 'py': 0, 'vx': 1, 'vy': 1}
        self.particles = pd.concat([self.particles, pd.DataFrame(new_particle, index=[0])])

    def move_particles(self, timestep):
        # move particles horizontally
        self.particles['px'] += self.particles['vx'] * timestep
        # check for horizontal overlaps with the bounding box
        x_overlap = (abs(self.particles['px']) + self.particles['r']) >= self.xlim
        # change velocity vector of horizontal overlaps
        self.particles['vx'].loc[x_overlap] *= -1
        # change position to correct post-collision (a posteriori)
        self.particles['px'].loc[x_overlap] += 2 * self.particles['vx'].loc[x_overlap] * timestep

        # same process for the y-axis
        self.particles['py'] += self.particles['vy'] * timestep
        y_overlap = (abs(self.particles['py']) + self.particles['r']) >= self.ylim
        self.particles['vy'].loc[y_overlap] *= -1
        self.particles['py'].loc[y_overlap] += 2 * self.particles['vy'].loc[y_overlap] * timestep


        # notes for adding inter-particle collision
        # project the points across several axes (x=0, y=0, y=x, y=-x?)
        # AND each axis to get every particle that is potentially colliding
        # and then brute-force among those

if __name__ == "__main__":
    # initialize a default 10x10 array, center of (0,0)
    pars = Particles(10, 10)

    # do all the particle adding here
    pars.add_particle(0, 1)

    # print the initial state
    # essential for getting the headers to plot
    print(f"time,{','.join(map(str,pars.particles.columns.to_list()))}")
    
    for i in range(0, 100):
        print(f"{i},{pars.particles.to_csv(index=False, header=False)}".strip())
        pars.move_particles(0.1)
