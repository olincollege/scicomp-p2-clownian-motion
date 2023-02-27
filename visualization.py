import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import data
df = pd.read_csv('data.csv')

frames = []
groups = df.groupby("time")
frame1 = groups.get_group((list(groups.groups)[0]))

for name, group in groups:
    frames.append(go.Frame(data=[go.Scatter(x=group["px"], y=group["py"], 
                                            mode="markers", marker={'size': group["r"], 
                                                                    'sizemode': 'diameter',
                                                                    'sizeref': 2.*max(group["r"])/11.**2}
    )])) 

# Build figure
fig = go.Figure(
    # Initalize markers at initial points
    data=[go.Scatter(x=frame1["px"], y=frame1["py"], mode="markers", marker={'size': [100]})],
    # Set layout of figure
    layout=go.Layout(
        xaxis=dict(range=[-7, 7], autorange=False),
        yaxis=dict(range=[-7, 7], autorange=False),
        width=600,
        height=600,
        # Add play button
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
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