import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

#uses a local python file called secrets.py that sets 
import secrets

#set up a plot to log hour by hour data
streams = [go.Stream(token=id_n, maxpoints = 24*3) for id_n in secrets.slow_stream_ids]
names = ["Tank", "In", "Out"]
traces = {name : go.Scatter(x=[], y=[], mode='lines+markers', stream=stream_n, name=name) for stream_n,name in zip(streams,names)}

data = go.Data(traces.values())

# Add title to layout object
layout = go.Layout(title='Daily', yaxis=dict(title='Temp'))

# Make a figure object
fig = go.Figure(data=data, layout=layout)

# Send fig to Plotly, initialize streaming plot, open new tab
py.iplot(fig, filename='Water Tank Daily')


#set up a plot to log minute by minute data
streams = [go.Stream(token=id_n, maxpoints = 24*60) for id_n in secrets.fast_stream_ids]
names = ["Tank", "In", "Out"]
traces = {name : go.Scatter(x=[], y=[], mode='lines+markers', stream=stream_n, name=name) for stream_n,name in zip(streams,names)}

data = go.Data(traces.values())

# Add title to layout object
layout = go.Layout(title='Hourly', yaxis=dict(title='Temp'))

# Make a figure object
fig = go.Figure(data=data, layout=layout)

# Send fig to Plotly, initialize streaming plot, open new tab
py.iplot(fig, filename='Water Tank Hourly')
