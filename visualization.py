import pandas as pd
import plotly.express as px

# Import data
df = pd.read_csv('data.csv')

fig = px.scatter(df, x="px", y="py", animation_frame="time", animation_group="n",
           size="r", range_x=[-7,7], range_y=[-7,7])

# Add borders of box
fig.add_shape(type="rect",
    xref="x", yref="y",
    x0=-5, y0=-5,
    x1=5, y1=5,
)

# TODO: Figure out how to specify circle sizes

fig.show()