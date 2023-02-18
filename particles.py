import numpy as np
from scipy import spatial as sp
import pandas as pd

class Particles:
    def __init__(self, xsize, ysize):
        self.particles = pd.DataFrame(columns=['n', 'r', 'px', 'py', 'vx', 'vy'])
        self.xlim = (-xsize/2, xsize/2)
        self.ylim = (-ysize/2, ysize/2)

    def add_particle(self, tag, r):
        new_particle = {'n': tag, 'r': r, 'px': 0, 'py': 0, 'vx': 1, 'vy': 1}
        self.particles = pd.concat([self.particles, pd.DataFrame(new_particle, index=[0])])

    def move_particles(self, timestep):
        self.particles['px'] += self.particles['vx'] * timestep
        self.particles['py'] += self.particles['vy'] * timestep




if __name__ == "__main__":
    pars = Particles(10, 10)
    pars.add_particle(0, 1)
    pars.add_particle(1, 1)
    pars.move_particles(0.5)
    print(pars.particles)
