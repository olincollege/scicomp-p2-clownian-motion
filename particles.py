import numpy as np
from scipy import spatial as sp
import pandas as pd

class Particles:
    def __init__(self, xsize, ysize):
        self.particles = pd.DataFrame(columns=['n', 'r', 'px', 'py', 'vx', 'vy'])
        self.xlim = xsize/2
        self.ylim = ysize/2

    def add_particle(self, tag, r):
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



if __name__ == "__main__":
    pars = Particles(10, 10)
    pars.add_particle(0, 1)
    for i in range(0, 100):
        print(f"TIMESTEP: {i} : -------------------------------------------")
        pars.move_particles(0.1)
        print(pars.particles)
