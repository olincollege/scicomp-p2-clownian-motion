import numpy as np
import pandas as pd
from scipy import spatial as sp


class Particles:
    def __init__(self, xsize, ysize):
        # name, radius, mass, x position, y position, x velocity, y velocity
        # includes dummy timestamp value to be changed later
        self.particles = pd.DataFrame(
            columns=["time", "n", "r", "m", "px", "py", "vx", "vy"], dtype=np.float64
        )

        # center box on (0,0)
        self.xlim = xsize / 2
        self.ylim = ysize / 2

    def add_particle(self, tag, r, m, px, py, vx, vy):
        # new_particle = pd.DataFrame([[tag, r, m, px, py, vx, vy]], columns=['n', 'r', 'm', 'px', 'py', 'vx', 'vy'])

        # # there may be a better way to do this?
        # self.particles = pd.concat([self.particles, new_particle], ignore_index=True)

        self.particles.loc[len(self.particles.index)] = [0, tag, r, m, px, py, vx, vy]

    def move_particles(self, timestep):
        # print(self.particles[['px', 'py']])
        pos_df = self.particles[["px", "py"]]
        pos = pos_df.to_numpy().astype(float)
        vel = self.particles[["vx", "vy"]].to_numpy()

        # these two are read-only
        masses = self.particles["m"].to_numpy()
        rad = self.particles["r"].to_numpy()

        # this only really works for particles with the same size
        # good enough for now, will accept suggestions on how to generalize
        thresholds = 2 * rad

        ## A PRIORI PARTICLE COLLISION
        # grab distances between particles
        distances = sp.distance.cdist(pos_df, pos_df)

        # create a map of colliding particles
        colliding = (0 < distances) & (distances <= thresholds)

        # calculate mass scalars
        mass_scalars = np.divide(
            (2 * np.matmul(colliding, masses)), (masses + np.matmul(colliding, masses))
        )

        # calculate velocity scalars
        delta = pos - np.matmul(colliding.astype(float), pos)
        dot = np.sum((vel - np.matmul(colliding, vel)) * (delta), axis=1)
        mag = np.square(np.sqrt(np.sum(np.square(delta), axis=1)))

        # reshape some vectors into arrays for multiplication purposes
        mass_scalars = np.reshape(mass_scalars, (mass_scalars.shape[0], 1))
        dot = np.reshape(dot, (dot.shape[0], 1))
        mag = np.reshape(mag, (mag.shape[0], 1))
        mag[mag == 0] = 0.001
        rad = np.reshape(rad, (rad.shape[0], 1))

        # update velocity vectors
        s1 = mass_scalars
        s2 = np.divide(dot, mag)
        s3 = delta
        vel -= s1 * s2 * s3
        # vel -= mass_scalars * np.transpose(np.divide(dot, mag)) * delta

        ## MOVE PARTICLES TO POST-PARTICLE COLLISION LOCATIONS
        pos += vel * float(timestep)

        ## A POSTERIORI WALL COLLISION
        # create 2d array to represent what particles overlap with what walls
        wall_overlapping = (abs(pos) + rad) >= [self.xlim, self.ylim]

        # take advantage of True == 1 & False == 0
        # (-2 * wall_overlapping + 1) converts True, False into Negative, Positive
        # so if wall_overlapping == True, that vector is inverted
        vel *= -2 * wall_overlapping + 1

        # move particles to where they should be post-collision
        pos += 2 * wall_overlapping * vel * timestep

        # ensure the particles array holds the new pos/vel values
        # to_numpy() does not guarantee that it returns a view rather than a copy
        #
        self.particles[["px", "py"]] = pos
        self.particles[["vx", "vy"]] = vel


if __name__ == "__main__":
    # initialize a default 10x10 array, center of (0,0)
    pars = Particles(10, 10)

    # do all the particle adding here
    for x in range(int(-pars.xlim) + 1, int(pars.xlim)):
        for y in range(int(-pars.ylim) + 1, int(pars.ylim)):
            if (y % 2 == 0) and (x % 2 == 0):
                pars.add_particle(
                    f"{x}{y}",
                    0.25,
                    1,
                    float(x),
                    float(y),
                    np.random.normal(scale=0.4),
                    np.random.normal(scale=0.4),
                )

    # essential for getting the headers to plot
    print(f"{','.join(map(str,pars.particles.columns.to_list()))}")

    for i in range(0, 5000):
        pars.particles["time"] = i
        # print(f"{i},{pars.particles.to_csv(index=False, header=False)}".strip())
        print(f"{pars.particles.to_csv(index=False,header=False)}".strip())
        pars.move_particles(0.005)
