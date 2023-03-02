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
            "args": [None, {"frame": {"duration": 50, "redraw": False},
                            "fromcurrent": True, "transition": {"duration": 25,
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

# Define slider attributes
# TODO: FINISH ADDING SLIDER 
slider_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Time:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 50, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

for name, group in groups:
    frames.append(go.Frame(data=[go.Scatter(x=group["px"], y=group["py"], 
                                            mode="markers", marker={'size': group["r"], 
                                                                    'sizemode': 'diameter',
                                                                    'sizeref': 2.*max(group["r"])/11.**2} # TODO: Look into using pi*r**2 to more accurately depict area
    )])) 

    slider_step = {"args": [
        [name],
        {"frame": {"duration": 50, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 25}}
    ],
        "label": name,
        "method": "animate"}
    
    slider_dict["steps"].append(slider_step)

# Build figure
fig = go.Figure(
    # Initalize markers at initial points
    data=[go.Scatter(x=frame1["px"], y=frame1["py"], mode="markers", marker={'size': group["r"], 
                                                                    'sizemode': 'diameter',
                                                                    'sizeref': 2.*max(group["r"])/11.**2})],
    # Set layout of figure
    layout=go.Layout(
        xaxis=dict(range=[-7, 7], autorange=False),
        yaxis=dict(range=[-7, 7], autorange=False),
        width=600,
        height=600,
        updatemenus=[menu_dict],
        sliders=[slider_dict]
    ),
    frames=frames
) 

# Add borders of box
fig.add_shape(type="rect",
    xref="x", yref="y",
    x0=-5, y0=-5,
    x1=5, y1=5
)

fig.show()

