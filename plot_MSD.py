import numpy as np
import pandas as pd
pd.options.plotting.backend = "plotly"

TIMESTEP_SIZE = 0.005

data = pd.read_csv('data.csv')

def get_dot(diff):
    return np.dot(diff, diff)

# add 1 since the first timestep is t=0
num_steps = data['time'].max() + 1

# initialize with a 0
# mean square displacement is 0 at t=0
# nothing has moved
msd_vals = [0]

this_time = data.loc[data['time'] == 0]
num_particles = len(this_time)
p0 = this_time[['px', 'py']].to_numpy()

for i in range(1, num_steps):
    this_time = data.loc[data['time'] == i]
    pi = this_time[['px', 'py']].to_numpy()
    diff = pi - p0
    dots = np.apply_along_axis(get_dot, 1, diff)
    msd = np.average(dots)
    msd_vals.append(msd)

time = [float(x)*TIMESTEP_SIZE for x in range(num_steps)]
msd_data = pd.Series(data=msd_vals, index=time)

fig = msd_data.plot(log_x=True, log_y=True)
fig.update_layout(
    title="Mean squared distance over time",
    xaxis_title="time",
    yaxis_title="MSD",
)
fig.show()
