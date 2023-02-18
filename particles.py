import numpy as np
import pandas as pd

class Particles:
    def __init__(self, xsize, ysize):
        self.particles = pd.DataFrame(columns=['n', 'r', 'p', 'v'])
        self.xlim = (-xsize/2, xsize/2)
        self.ylim = (-ysize/2, ysize/2)

    def add_particle(self, tag, r):
        new_position = np.array([0, 0])
        new_velocity = np.array([1, 1])
        new_particle = {'n': tag, 'r': r, 'p': [new_position], 'v': [new_velocity]}
        self.particles = pd.concat([self.particles, pd.DataFrame(new_particle)])

    def move_particles(self, timestep):
        self.particles['p'] += self.particles['v'] * timestep




if __name__ == "__main__":
    pars = Particles(10, 10)
    pars.add_particle(0, 1)
    pars.add_particle(1, 1)
    pars.move_particles(0.5)
    print(pars.particles)

