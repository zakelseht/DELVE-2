# Plotly packages
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.graph_objects as go

# Bokeh packages
# from bokeh.io import output_file, show
# from bokeh.models import ColumnDataSource, FactorRange
# from bokeh.plotting import figure, output_file, show
# from bokeh.embed import components
# from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
# import bokeh
# Standard Libraries
import pandas as pd
from datetime import datetime
import requests
from datetime import date
from random import randint

rowEvenColor = 'lightgrey'
rowOddColor = 'turquoise'
# def bokeh_3d_plot():
#     x= [1,3,5,7,9,11,13]
#     y= [1,2,3,4,5,6,7]
#     title = 'y = f(x)'

#     plot = figure(title= title , 
#         x_axis_label= 'X-Axis', 
#         y_axis_label= 'Y-Axis', 
#         plot_width =400,
#         plot_height =400)

#     plot.line(x, y, legend= 'f(x)', line_width = 2)
#     script, div = components(plot)
#     return script, div

# def bokeh_table(x_title = '', y_title = '', data = dict(dates=[date(2014, 3, i+1) for i in range(10)]), heat = None, units = None):
#     # ColumnDataSource() used if you want to use built in features like hover over
#     data.index.name = 'Treatment'
#     data.columns.name = 'Prediction'    
#     source = ColumnDataSource(data)

#     columns = [
#         TableColumn(field="dates", formatter=DateFormatter()),
#         TableColumn(field="downloads", title="Downloads"),
#     ]
#     table_figure = DataTable(source=source, columns=columns, width=400, height=280)
#     script, div = components(table_figure)
    
#     return script, div

def get_data():
    # LINK DEPRICATED: JSON EMPTY
    url = 'https://api.unibit.ai/historicalstockprice/AAPL?range=3m&interval=2&AccessKey=demo'
    res = requests.get(url)
    res = res.json()['Stock price']
    return res

def get_simple_candlestick():
    data = get_data()
    x,y,z,w,k=[],[],[],[],[]
    for item in data:
        x.append(item['date']),
        y.append(item['open']),
        z.append(item['high']),
        w.append(item['low']),
        k.append(item['close'])

    trace1 = go.Candlestick(
        x=x,
        open = y,
        high = z,
        low = w,
        close = k
    )
    layout = go.Layout(
        # autosize=True,
        # width = 800,
        # height=900,
        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )
    plot_data = [trace1]
    figure = go.Figure(data=plot_data, layout=layout)
    plot_div = plot(figure, output_type='div', include_plotlyjs=False)
    return plot_div

def get_topographical_3D_surface_plot():
    raw_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

    data = [go.Surface(z=raw_data.as_matrix())]

    layout = go.Layout(

        autosize=False,
        width=800,
        height=700,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
            )
        )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div',filename='elevations-3d-surface')
    
    return plot_div

def get_synergies(matrix):
    data = [go.Surface(z=matrix,
            # colorscale='earth',  
            colorscale=[
                        [0.0, "rgb(158, 0, 0)"],
                        [.7, "rgb(172, 175, 172)"],
                        [1.0, "rgb(40, 239, 9)"]
                        ],
            )]

    layout = go.Layout(
        autosize=False,
        width=800,
        height=700,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
            )
        )

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div',filename='elevations-3d-surface')

    return plot_div

