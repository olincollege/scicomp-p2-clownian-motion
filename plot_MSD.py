"""Outputs a plot showing the relationship between the log of the mean square displacement to log of time."""

import numpy as np
import pandas as pd


def get_dot(diff):
    """Returns dot product of two vectors."""
    return np.dot(diff, diff)

# Activate plotting backend
pd.options.plotting.backend = "plotly"

# Set timestep size
TIMESTEP_SIZE = 0.005

# Import data
data = pd.read_csv('data.csv')

# Set first timestep to 0
num_steps = data['time'].max() + 1

# Set mean square displacement to 0 at timestep 0
msd_vals = [0]

this_time = data.loc[data['time'] == 0]
num_particles = len(this_time)
p0 = this_time[['px', 'py']].to_numpy()

# Calculate mean square displacement at each timestep
for i in range(1, num_steps):
    this_time = data.loc[data['time'] == i]
    pi = this_time[['px', 'py']].to_numpy()
    diff = pi - p0
    dots = np.apply_along_axis(get_dot, 1, diff)
    msd = np.average(dots)
    msd_vals.append(msd)

# Create plot of the log of the mean square displacement to log of time
time = [float(x)*TIMESTEP_SIZE for x in range(num_steps)]
msd_data = pd.Series(data=msd_vals, index=time)

fig = msd_data.plot(log_x=True, log_y=True)
fig.update_layout(
    title="Mean squared distance over time",
    xaxis_title="time",
    yaxis_title="MSD",
)
fig.show()
