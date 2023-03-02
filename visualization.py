import pandas as pd
import plotly.express as px

# Import data
df = pd.read_csv('data.csv')

# TODO: Create area radius
df["a"] = df["r"]*5

# Create scatter plot
fig = px.scatter(df, 
                 x="px", 
                 y="py", 
                 animation_frame="time", 
                 animation_group="n",
                 size="a", 
                 range_x=[-7,7], 
                 range_y=[-7,7],
                 width=600, 
                 height=600
)

# Add borders of box
fig.add_shape(type="rect",
              xref="x", 
              yref="y",
              x0=-5, 
              y0=-5,
              x1=5,
              y1=5
)

fig.update_layout(transition = {'duration': 0.001})

fig.show()

