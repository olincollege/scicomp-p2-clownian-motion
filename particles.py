import numpy as np
import pandas as pd
from scipy import spatial as sp


class Particles:
    def __init__(self, xsize: int, ysize: int):
        """Stores particle information and dimensions of the simulation."""
        # Initialize dataframe to store all particles in the simulation
        self.particles = pd.DataFrame( 
            columns=["time", 
                     "n", # id
                     "r", # radius
                     "m", # mass
                     "px", # x position
                     "py", # y position
                     "vx", # x velocity
                     "vy"], # y velocity
                     dtype=np.float64
        )

        # Center box on (0,0)
        self.xlim = xsize / 2
        self.ylim = ysize / 2

    def add_particle(self, tag: str, r: float, m: int, px: float, py: float, vx: float, vy: float):
        """Adds particle to the simulation.
        
        Args: 
            tag (str): particle ID
            r (float): radius
            m (int): mass
            px (float): x position
            py (float): y position
            vx (float): x velocity
            vy (float): y velocity
        """
        self.particles.loc[len(self.particles.index)] = [0, tag, r, m, px, py, vx, vy]

    def move_particles(self, timestep: float):
        """Handle all collisions and particle movements during a single timestep.
        
        Args: 
            timestep (float): change in time 
        """
        # Get position, velocity, mass, and radius information
        pos_df = self.particles[["px", "py"]]
        pos = pos_df.to_numpy().astype(float)
        vel = self.particles[["vx", "vy"]].to_numpy()
        masses = self.particles["m"].to_numpy()
        rad = self.particles["r"].to_numpy()

        # Calculate distance at which particles collide (note: this only really works for particles with the same size)
        thresholds = 2 * rad

        # Get distances between particles
        distances = sp.distance.cdist(pos_df, pos_df)

        # Create a bitmap of colliding particles
        colliding = (0 < distances) & (distances <= thresholds)

        # Calculate mass scalars
        mass_scalars = np.divide(
            (2 * np.matmul(colliding, masses)), (masses + np.matmul(colliding, masses))
        )

        # Calculate velocity scalars
        delta = pos - np.matmul(colliding.astype(float), pos)
        dot = np.sum((vel - np.matmul(colliding, vel)) * (delta), axis=1)
        mag = np.square(np.sqrt(np.sum(np.square(delta), axis=1)))

        # Reshape vectors into arrays for multiplication purposes
        mass_scalars = np.reshape(mass_scalars, (mass_scalars.shape[0], 1))
        dot = np.reshape(dot, (dot.shape[0], 1))
        mag = np.reshape(mag, (mag.shape[0], 1))
        mag[mag == 0] = 0.001
        rad = np.reshape(rad, (rad.shape[0], 1))

        # Update velocity vectors
        s1 = mass_scalars
        s2 = np.divide(dot, mag)
        s3 = delta
        vel -= s1 * s2 * s3

        # Update positions
        pos += vel * float(timestep)

        # Create a bitmap of particles that collide with walls
        wall_overlapping = (abs(pos) + rad) >= [self.xlim, self.ylim]

        # Update velocity vectors by inverting velocity vector if particle collides with a wall 
        vel *= -2 * wall_overlapping + 1

        # Update positions
        pos += 2 * wall_overlapping * vel * timestep

        # Update particles array with new position and velocity values
        self.particles[["px", "py"]] = pos
        self.particles[["vx", "vy"]] = vel


if __name__ == "__main__":
    # Initialize a default 10x10 array, center of (0,0)
    pars = Particles(10, 10)

    # Add particles to simulation
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

    # Print headers of dataframe
    print(f"{','.join(map(str,pars.particles.columns.to_list()))}")

    # Loop through 5000 timesteps
    for i in range(0, 5000):
        pars.particles["time"] = i
        # Print particle information
        print(f"{pars.particles.to_csv(index=False,header=False)}".strip())
        # Move particles one timestep
        pars.move_particles(0.005)
