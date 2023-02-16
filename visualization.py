# Source: https://plotly.com/python/animations/

import pandas as pd
import plotly.express as px

# Initialize test data 
data = {'ind': [0, 0 , 0, 0],
        'time': [0, 1, 2, 3],
        'x': [3, 3.25, 3.5, 3.75], 
        'y': [5, 5.25, 5.5, 5.75],
        'r': [1, 1, 1, 1]}

df = pd.DataFrame(data)

fig = px.scatter(df, x="x", y="y", animation_frame="time", animation_group="ind",
           size="r", range_x=[0,10], range_y=[0,10])

fig.show()