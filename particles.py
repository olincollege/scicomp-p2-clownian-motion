import numpy as np
from scipy import spatial as sp
import pandas as pd

class Particles:
    def __init__(self, xsize, ysize):
        # name, radius, x position, y position, x velocity, y velocity
        self.particles = pd.DataFrame(columns=['n', 'r', 'px', 'py', 'vx', 'vy'])
        # center box on (0,0)
        self.xlim = xsize/2
        self.ylim = ysize/2

    def add_particle(self, tag, r):
        new_particle = {'n': tag, 'r': r, 'px': -3.9, 'py': 0, 'vx': 1, 'vy': 1}

        # there may be a better way to do this?
        self.particles = pd.concat([self.particles, pd.DataFrame(new_particle, index=[0])])

    def move_particles(self, timestep):
        pos = self.particles[['px','py']].to_numpy()
        vel = self.particles[['vx','vy']].to_numpy()
        rad = self.particles['r'].to_numpy()

        pos += vel * timestep

        # create two overlap columns 
        overlap = (abs(pos) + rad) >= [self.xlim, self.ylim]

        # take advantage of True == 1 & False == 0
        # (-2 * overlap + 1) converts True, False into Negative, Positive
        # so if overlap == True, that vector is inverted
        vel *= (-2 * overlap + 1)

        # a posteriori move particles to where they should be post-collision
        pos += 2 * overlap * vel * timestep

        # ensure the particles array holds the new pos/vel values
        # to_numpy() does not guarantee that it returns a view rather than a copy
        self.particles[['px', 'py']] = pos
        self.particles[['vx', 'vy']] = vel
        
if __name__ == "__main__":
    # initialize a default 10x10 array, center of (0,0)
    pars = Particles(10, 10)

    # do all the particle adding here
    pars.add_particle(0, 1)

    # essential for getting the headers to plot
    print(f"time,{','.join(map(str,pars.particles.columns.to_list()))}")
    
    for i in range(0, 50):
        print(f"{i},{pars.particles.to_csv(index=False, header=False)}".strip())
        pars.move_particles(0.1)
