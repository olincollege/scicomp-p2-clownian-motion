"""Outputs an animated simulation of the particles moving over time."""

import pandas as pd
import plotly.graph_objects as go


# Import data
df = pd.read_csv('data.csv')

frames = []
groups = df.groupby("time")
frame1 = groups.get_group((list(groups.groups)[0]))

# Define menu attributes
menu_dict = {
    "buttons": [ 
        { # Add play button
            "args": [None, {"frame": {"duration": 0.1, "redraw": False},
                            "fromcurrent": True, "transition": {"duration": 0.1,
                                                                "easing": "quadratic-in-out"}}],
            "label": "Play",
            "method": "animate"
        },
        { # Add pause button
            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}}],
            "label": "Pause",
            "method": "animate"
        }
    ],
    "direction": "left",
    "pad": {"r": 10, "t": 87},
    "showactive": False,
    "type": "buttons",
    "x": 0.1,
    "xanchor": "right",
    "y": 0,
    "yanchor": "top"
}

# Create frames representing particles at each timestep
for name, group in groups:
    frames.append(go.Frame(data=[go.Scatter(x=group["px"], y=group["py"], 
                                            mode="markers", marker={'size': group["r"], 
                                                                    'sizemode': "diameter",
                                                                    'sizeref': 2*max(group["r"])/5.5**2} 
    )])) 

# Build figure
fig = go.Figure(
    # Initalize markers at initial points
    data=[go.Scatter(x=frame1["px"], y=frame1["py"], mode="markers", marker={'size': group["r"], 
                                                                    'sizemode': 'diameter',
                                                                    'sizeref': 2*max(group["r"])/5.5**2})],
    # Set layout of figure
    layout=go.Layout(
        xaxis=dict(range=[-7, 7], autorange=False),
        yaxis=dict(range=[-7, 7], autorange=False),
        width=600,
        height=600,
        updatemenus=[menu_dict],
    ),
    frames=frames
) 

# Add borders of bounding box
fig.add_shape(type="rect",
    xref="x", yref="y",
    x0=-5, y0=-5,
    x1=5, y1=5
)

fig.show()