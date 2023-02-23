import numpy as np
import pandas as pd
from scipy import spatial as sp

data = {'x': [5, 5, 1, 9],
        'y': [5, 6, 1, 9],
        'vx': [1, -1, 1, 0],
        'vy': [1, -1, 0, 1],
        'm': [2, 4, 2, 2],
        'r': [0.5, 0.5, 0.5, 0.5]}

df = pd.DataFrame(data)
pos_df = df[['x', 'y']]
rad_df = df[['r']]

# Distance between spheres 
cdist = sp.distance.cdist(pos_df, pos_df)

# Radius of spheres
thresh = 2*rad_df.to_numpy()

# Map of colliding spheres
map = (0 < cdist) & (cdist <= thresh)

# Calculate post-collision velocities
v = df[['vx', 'vy']].to_numpy()

# Calculate mass scalars
m = df[['m']].to_numpy()
b = np.divide((2 * np.matmul(map, m)), (m + np.matmul(map, m)))

# Calculate velocity scalars
x = pos_df.to_numpy()
c = np.sum((v - np.matmul(map, v)) * ((x - np.matmul(map, x))), axis=1) # dot 
d = np.square(np.sqrt(np.sum(np.square((x - np.matmul(map, x))), axis=1)))
e = np.divide(c, d)

# Difference in positions
f = x - np.matmul(map, x)

output = v - np.transpose(np.transpose(b) * e) * f
print(output)
