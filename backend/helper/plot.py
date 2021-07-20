# === Plotly packages === 
# import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.tools import FigureFactory as FF
import plotly.express as px
# from plotly.plotly import image

# === Bokeh packages ===
# from bokeh.io import output_file, show
# from bokeh.models import ColumnDataSource, FactorRange
# from bokeh.plotting import figure, output_file, show
# from bokeh.embed import components
# from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
# import bokeh

# === Standard Libraries ===
import pandas as pd
from datetime import datetime
import requests
from datetime import date
from random import randint
import numpy as np
from . import tox_plot
from delve import models
import matplotlib.pyplot as plt
import scipy

# === Django ===
from django.db.models import Q

np.random.seed(1)

rowEvenColor = 'lightgrey'
rowOddColor = 'teal'
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
#     return div

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
    plot_div = plot(fig, output_type = 'div',filename = 'elevations-3d-surface')

    return plot_div
def get_synergies_2d(matrix):
    pass

def get_combo(matrix, x=None, y=None):
    # if x.any():
    #     pass
    # if y.any():
    #     pass
    data = [go.Surface(
            z=matrix,
            colorscale='earth',  
            # colorscale="Viridis",
            )]

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=False,
        width=600,
        height=500,
        # margin=go.layout.Margin(
        #     # l=200,
        #     # r=50,
        #     # b=100,          
        #     # t=100,
        #     # pad=4
        # )
        )
    
    fig = go.Figure(data=data, layout=layout)

    # if x.any():
    #     fig.update_xaxes(range=x)
    # if y.any():
    #     fig.update_yaxes(range=y)

    plot_div = plot(fig, output_type = 'div',filename = 'elevations-3d-surface')
    
    
    # fig.show()
    return plot_div

def ic50_graph(df, axis=0):
    # df = tox_plot.df_format(df)
    dose1, dose2, _, _, _, _, viability1, viability2 = tox_plot.df_components(df)

    if axis:
        concentration = dose1
        viab = viability1
    else:
        concentration = dose2
        viab = viability2

    data = [go.Scatter(
        x = -np.log10(concentration),
        y = (viab),
    )]

    layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    # plot_bgcolor='rgba(0,0,0,0)',    
    autosize=False,
    width=500,
    height=500,
    margin=go.layout.Margin(
            l=50,
            r=50,
            b=100,          
            t=100,
            pad=4
        ))

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', filename='2d-surface')

    return plot_div



# =========================================================================================================
# Built to work for REST api calls or just general calls, ones above will be deprecated
# =========================================================================================================
def API_Synergy(id):

    combo = models.Combo.objects.get(pk=id)
    print(combo)
    print(combo.df_pickled)
    matrix = combo.get_df()
    print("matrix",matrix)
    data = [go.Surface(
            z=matrix,
            colorscale='earth',  
            )]

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=False,
        width=600,
        height=500,
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=4
    ),
        )
    
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type = 'div',filename = 'elevations-3d-surface')
    # img_bytes = image.get(fig)
    return plot_div

def API_ML_model(id):
    # Call NN model to get cyto
    # matrix = cyto 
    matrix = False
    data = [go.Surface(
            z=matrix,
            colorscale='earth',  
            )]

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=False,
        width=600,
        height=500,
        )
    
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div

def API_indications(cellLine):
    # Call NN model to get cyto
    # matrix = cyto 
    matrix = False
    data = [go.Surface(
            z=matrix,
            colorscale='earth',  
            )]

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=False,
        width=600,
        height=500,
        )
    
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div

def API_ic50(df, axis=0):
    dose1, dose2, _, _, _, _, viability1, viability2 = tox_plot.df_components(df)

    if axis:
        concentration = dose1
        viab = viability1
    else:
        concentration = dose2
        viab = viability2

    data = [go.Scatter(
        x = -np.log10(concentration),
        y = (viab),
    )]

    layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    autosize=False,
    width=500,
    height=500,
    margin=go.layout.Margin(
            l=50,
            r=50,
            b=100,          
            t=100,
            pad=4,
        ))

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', filename='2d-surface')

    return plot_div

    
def graph_img(id):
    combo = models.Combo.objects.get(pk=id)
    print(combo)
    print(combo.df_pickled)
    matrix = combo.get_df()
    print("matrix",matrix)
    data = [go.Surface(
            z=matrix,
            colorscale='earth',  
            )]

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=False,
        width=600,
        height=500,
        )
    
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, auto_open=False, image = 'png', output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
    # return plot(fig, auto_open=True, image = 'png', 
    #             image_filename=str(combo.name)+'plot_image', output_type='file', 
    #             image_width=800, image_height=600, filename=str(combo.name)+'_report_cover.html', validate=False)

def histogram(dictionary, title):
    dictionary = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}
    fig = go.Figure(
        data=[go.Bar(x=list(dictionary.keys()), y=list(dictionary.values()))]
        )

    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))
    # fig.update_xaxes(tickangle=45)
    fig.update_layout(
        height=500,
        title={
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f",
    ))

    print(fig)
    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div


# def ic50_efficacy_chart(id, title):
# What drug is most effective with another drug

# ================================================================================================================================================================================================================================
def leading_drugs_all_scores():
### PART 1: best drug_2 with given drug                     "this drug has worked best with thid drg"
### visualises effectiveness of drug relative to top 10   
### synergy score vs drug_2 name
### PART 2: best avg_score for drug_1 for an indiciation    "this drug tends to perform well with other drugs on this indication"
 
    # get combo and top combos
    top_combos = models.Combo.objects.order_by('Chou_score')[::-1][2:10]
 
    drug_lst     = [c.drug_1.drug_name for c in top_combos]     # x-axis
    chou_lst     = [c.Chou_score for c in top_combos]           # y-axis
    bliss_lst    = [c.Bliss_score for c in top_combos]          # y-axis
    hsa_lst      = [c.HSA_score for c in top_combos]            # y-axis
    loewe_lst    = [c.Loewe_score for c in top_combos]          # y-axis
    zip_lst      = [c.ZIP_score for c in top_combos]            # y-axis
    # setup figure using plotly
    # data=[go.Bar(x=drug_list, y=list(c.Chou_score for c in top_combos))]

    fig = make_subplots()

    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))

    # Add traces
    fig.add_trace(
        go.Bar(x = drug_lst, y = chou_lst, name = "Chou"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x = drug_lst, y = bliss_lst, name="Bliss"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x = drug_lst, y = hsa_lst, name="HSA"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x = drug_lst, y = loewe_lst, name="Loewe"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x = drug_lst, y = zip_lst, name="ZIP"),
        secondary_y=False,
    )
    # fig.add_trace(
    #     go.Bar(x=list(c.name for c in top_combos), y=list(c.Chou_score for c in top_combos), name="yaxis2 data"),
    #     secondary_y=True,
    # )
    fig.update_layout(
        title={
            'text': 'Leading Drugs (all scores)',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f",
    ))


    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div


# ================================================================================================================================================================================================================================
def leading_drugs_w_avg():
### PART 1: best drug_2 with given drug                     "this drug has worked best with thid drg"
### visualises effectiveness of drug relative to top 10   
### synergy score vs drug_2 name
### PART 2: best avg_score for drug_1 for an indiciation    "this drug tends to perform well with other drugs on this indication"
 
    # get combo and top combos
    top_combos = models.Combo.objects.order_by('Chou_score')[::-1][2:15]
 
    drug_lst     = [c.drug_1.drug_name for c in top_combos]         # x-axis
    avg_chou_lst     = [c.Chou_score for c in top_combos]   # y-axis
    total_avg_chou = np.sum(avg_chou_lst)/len(avg_chou_lst)

    # setup figure using plotly

    fig = make_subplots()
    labels = {'Total Avg Chou': (0,total_avg_chou)}
    line_color = "LightSeaGreen"

    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))

    # Add traces
    fig.add_trace(
        go.Bar(
            x = drug_lst, 
            y = avg_chou_lst, 
            name = "Chou"),
        secondary_y=False,
    )


    # Add shapes
    fig.add_trace(
        go.Scatter(
            x = drug_lst,
            y = [total_avg_chou],
            name="Total Avg Chou",
            marker_color = line_color,
            mode = "lines"),
        secondary_y=False,
    )
            
    fig.update_layout(
        title={
            'text': 'Leading Drugs by Chou (w/ Avg)',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"),
        shapes=[
            dict(
            # Line reference to the axes
                type="line",
                yref="y",
                xref= 'paper',
                x0=0,
                y0=total_avg_chou,
                # x1=drug_lst[-1],
                x1=1,
                y1=total_avg_chou,
                line=dict(
                    color=line_color,
                    width=3,
                ),
            )],
        )

    # fig.show()
    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# ================================================================================================================================================================================================================================
def t_distrib():
    # 3 KINDS:
    # FIRST: t distribution of drug performance in an indication, x axis is drug                                             "In this indication these were the performances "
    # SECOND: t distribtuion of the combo vs other combos (checks to see how rare the top synergies are), x axis are combos, "These are promising drug combinations for this drug"
    # THIRD: t distribtuion of the combo vs other combos (checks to see how rare the top synergies are), x axis are combos,  "These are promising drug combinations in general"
    ####

    top_combos = models.Combo.objects.order_by('Chou_score')[::-1][2:]
    avg_chou_lst  = [c.Chou_score for c in top_combos]
    total_avg_chou = np.sum(avg_chou_lst)/len(avg_chou_lst)
    # print(len(avg_chou_lst))
    # Let us generate some random data from the Normal Distriubtion. We will sample 50 points from a normal distribution with mean μ=0 and variance σ2=1 and from another with mean μ=2 and variance σ2=1.
    
    y1 = scipy.stats.norm.pdf(avg_chou_lst, loc=total_avg_chou)

    trace1 = go.Scatter(
        x = avg_chou_lst,
        y = y1,
        name='Mean of 0',
        mode = "lines"
    )


    data = [trace1]

    fig = go.Figure(
        data=[d for d in data]
        )

    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))
    # fig.update_xaxes(tickangle=45)
    percentile = np.percentile(avg_chou_lst, 90)
    fig.update_layout(
        title={
            'text': 'title',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"),
        shapes=[
            dict(
            # Line reference to the axes
                type="line",
                xref="x",
                yref="y",
                x0=percentile,
                y0=0.0,
                x1=percentile,
                y1=0.5,
                line=dict(
                    width=3,
                ),
            )],
    )


    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# ================================================================================================================================================================================================================================
def scatter_highlight_clusters():
    x0 = np.random.normal(2, 0.4, 400)
    y0 = np.random.normal(2, 0.4, 400)
    x1 = np.random.normal(3, 0.6, 600)
    y1 = np.random.normal(6, 0.4, 400)
    x2 = np.random.normal(4, 0.2, 200)
    y2 = np.random.normal(4, 0.4, 200)

    # Create figure
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=x0,
            y=y0,
            mode="markers",
            marker=dict(color="DarkOrange")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x1,
            y=y1,
            mode="markers",
            marker=dict(color="Crimson")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x2,
            y=y2,
            mode="markers",
            marker=dict(color="RebeccaPurple")
        )
    )

    # Add buttons that add shapes
    cluster0 = [dict(type="circle",
                                xref="x", yref="y",
                                x0=min(x0), y0=min(y0),
                                x1=max(x0), y1=max(y0),
                                line=dict(color="DarkOrange"))]
    cluster1 = [dict(type="circle",
                                xref="x", yref="y",
                                x0=min(x1), y0=min(y1),
                                x1=max(x1), y1=max(y1),
                                line=dict(color="Crimson"))]
    cluster2 = [dict(type="circle",
                                xref="x", yref="y",
                                x0=min(x2), y0=min(y2),
                                x1=max(x2), y1=max(y2),
                                line=dict(color="RebeccaPurple"))]

    fig.update_layout(
        updatemenus=[
            dict(buttons=list([
                dict(label="None",
                    method="relayout",
                    args=["shapes", []]),
                dict(label="Cluster 0",
                    method="relayout",
                    args=["shapes", cluster0]),
                dict(label="Cluster 1",
                    method="relayout",
                    args=["shapes", cluster1]),
                dict(label="Cluster 2",
                    method="relayout",
                    args=["shapes", cluster2]),                     
                dict(label="All",
                    method="relayout",
                    args=["shapes", cluster0 + cluster1 + cluster2])
            ]),
            )
        ]
    )

    # Update remaining layout properties
    fig.update_layout(
        title_text="Highlight Clusters",
        showlegend=False,
    )

    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# ================================================================================================================================================================================================================================
def update_dropdown():
    # Load dataset
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
    df.columns = [col.replace("AAPL.", "") for col in df.columns]

    # Initialize figure
    fig = go.Figure()

    # Add Traces

    fig.add_trace(
        go.Scatter(x=list(df.index),
                y=list(df.High),
                name="High",
                line=dict(color="#33CFA5")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                y=[df.High.mean()] * len(df.index),
                name="High Average",
                visible=False,
                line=dict(color="#33CFA5", dash="dash")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                y=list(df.Low),
                name="Low",
                line=dict(color="#F06A6A")))

    fig.add_trace(
        go.Scatter(x=list(df.index),
                y=[df.Low.mean()] * len(df.index),
                name="Low Average",
                visible=False,
                line=dict(color="#F06A6A", dash="dash")))

    # Add Annotations and Buttons
    high_annotations = [dict(x="2016-03-01",
                            y=df.High.mean(),
                            xref="x", yref="y",
                            text="High Average:<br> %.3f" % df.High.mean(),
                            ax=0, ay=-40),
                        dict(x=df.High.idxmax(),
                            y=df.High.max(),
                            xref="x", yref="y",
                            text="High Max:<br> %.3f" % df.High.max(),
                            ax=0, ay=-40)]
    low_annotations = [dict(x="2015-05-01",
                            y=df.Low.mean(),
                            xref="x", yref="y",
                            text="Low Average:<br> %.3f" % df.Low.mean(),
                            ax=0, ay=40),
                    dict(x=df.High.idxmin(),
                            y=df.Low.min(),
                            xref="x", yref="y",
                            text="Low Min:<br> %.3f" % df.Low.min(),
                            ax=0, ay=40)]

    fig.update_layout(
        xaxis = dict(
                    tickmode = 'linear',
                    tick0 = 0.5,
                    dtick = 10
            ),  
        updatemenus=[
            dict(
                active=0,
                dtick = 0.75,
                buttons=list([
                    dict(label="None",
                        method="update",
                        args=[{"visible": [True, False, True, False]},
                            {"title": "Yahoo",
                                "annotations": []}]),
                    dict(label="High",
                        method="update",
                        args=[{"visible": [True, True, False, False]},
                            {"title": "Yahoo High",
                                "annotations": high_annotations}]),
                    dict(label="Low",
                        method="update",
                        args=[{"visible": [False, False, True, True]},
                            {"title": "Yahoo Low",
                                "annotations": low_annotations}]),
                    dict(label="Both",
                        method="update",
                        args=[{"visible": [True, True, True, True]},
                            {"title": "Yahoo",
                                "annotations": high_annotations + low_annotations}]),
                ]),
            )
        ])

    # Set title
    fig.update_layout(title_text="Yahoo")
    
    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# ================================================================================================================================================================================================================================
def leading_cellLine_for_drug(drug_id=2):
    # filter combos for a drug, get celline from leading combo
    drug_searched = models.Drug.objects.get(id=drug_id)
    top_combos = models.Combo.objects.filter(
        Q(drug_1__id = drug_id) | Q(drug_2__id = drug_id)
    ).distinct("Chou_score").order_by("Chou_score", "id")
 
    # x axis (bins)
    cellLine_lst = [c.CellLine.cell_line for c in top_combos]
    # y axis
    chou_score_lst = [c.Chou_score for c in top_combos]

    # setup figure using plotly

    fig = make_subplots()
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))

    # Add traces
    fig.add_trace(
        go.Bar(
            x = cellLine_lst, 
            y = chou_score_lst, 
            name = "Chou"),
        secondary_y=False,
    )      

    fig.update_layout(
        title={
            'text': 'Leading Cell Line for '+drug_searched.get_code_name(),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Chou Scores",
        xaxis_title="Cell Lines",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f",
    ))


    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# ================================================================================================================================================================================================================================
def leading_cellLine_for_combo(combo_id=1):
    # filter combos for a drug, get celline from leading combo
    combo_searched = models.Combo.objects.get(id=combo_id)
    drug_1 = combo_searched.drug_1
    drug_2 = combo_searched.drug_2
    top_combos = models.Combo.objects.filter(
        Q(drug_1__id = drug_1.id) & Q(drug_2__id = drug_2.id) | Q(drug_1__id = drug_2.id) & Q(drug_2__id = drug_1.id),
    ).distinct("Chou_score").order_by("Chou_score", "id")
    # x axis (bins)
    cellLine_lst = [c.CellLine.cell_line for c in top_combos]
    # y axis
    chou_score_lst = [c.Chou_score for c in top_combos]

    # setup figure using plotly

    fig = make_subplots()
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))

    # Add traces
    fig.add_trace(
        go.Bar(
            x = cellLine_lst, 
            y = chou_score_lst, 
            name = "Chou"),
        secondary_y=False,
    )      

    fig.update_layout(
        title={
            'text': 'Leading Cell Lines for Drugs '+drug_1.get_code_name()+" and "+drug_2.get_code_name(),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Chou Scores",
        xaxis_title="Cell Lines",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f",
    ))


    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# ================================================================================================================================================================================================================================
def leading_indication_for_drug(drug_id=1):
    # filter combos for a drug, get celline from leading combo
    drug_searched = models.Drug.objects.get(id=drug_id)
    top_combos = models.Combo.objects.filter(
        Q(drug_1__id = drug_id) | Q(drug_2__id = drug_id)
    ).distinct("Chou_score").order_by("Chou_score", "id")[::-1]
    
    if top_combos[0].Chou_score > 25:
        top_combos = top_combos[1::]
    print(top_combos[0].Chou_score)
    print(top_combos[0].CellLine.indication)
    # sort it
    # x axis (bins)
    indication_lst = [c.CellLine.indication.cancer_name for c in top_combos]
    # y axis
    chou_score_lst = [c.Chou_score for c in top_combos]


    # setup figure using plotly
    # fig = go.Figure()
    # fig.add_trace(go.Histogram(histfunc="avg", y=chou_score_lst, x=indication_lst, name="count"))
    # fig.show()

    fig = make_subplots()
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))

    # Add traces
    fig.add_trace(
        go.Bar(
            x = indication_lst, 
            y = chou_score_lst, 
            offsetgroup=1,
            name = "Chou"),
        secondary_y=False,
    )      

    fig.update_layout(
        barmode='overlay',
        title={
            'text': 'Leading Indications for '+drug_searched.get_code_name(),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Chou Scores",
        xaxis_title="Indications",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f",
    ))


    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    fig.show()
    return plot_div
# ================================================================================================================================================================================================================================
def leading_combos_for_drug(drug_id=1):
    # filter combos for a drug, get celline from leading combo
    leading_combos_dict = {}
    drug_searched = models.Drug.objects.get(id=drug_id)
    top_combos = models.Combo.objects.filter(
        Q(drug_1__id = drug_id) | Q(drug_2__id = drug_id)
    ).distinct("Chou_score").order_by("Chou_score", "id")[::-1]
    
    # gets rid of 10x10 edge report but this is messy and bad idea
    if top_combos[0].Chou_score > 25:
        top_combos = top_combos[1::]
    
    leading_combos_dict['Report Name'] = [c.name for c in top_combos]
    leading_combos_dict['Chou Score'] = [c.Chou_score for c in top_combos]
    leading_combos_dict['Drug 1'] = [c.drug_1 for c in top_combos]
    leading_combos_dict['Drug 2'] = [c.drug_2 for c in top_combos]
    leading_combos_dict['Cell Line'] = [c.CellLine for c in top_combos]

    # setup figure using plotly
    df = pd.DataFrame.from_dict(leading_combos_dict)

    import tempfile
    import webbrowser

    html =  df.to_html()

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(html)
    webbrowser.open(url)

    return 
# ================================================================================================================================================================================================================================
def leading_ic50s_for_drug(drug_id=1):
    # filter combos for a drug, get celline from leading combo
    leading_combos_dict = {}
    drug_searched = models.Drug.objects.get(id=drug_id)
    print(drug_searched.name)
    top_combos = models.Ic50.objects.filter(
        Q(drug1_id = drug_id)
    ).order_by("effect")[::-1]
    
    # gets rid of 10x10 edge report but this is messy and bad idea
    if top_combos[0].Chou_score > 25:
        top_combos = top_combos[1::]
    
    leading_combos_dict['Report Name'] = [c.name for c in top_combos]
    leading_combos_dict['Chou Score'] = [c.Chou_score for c in top_combos]
    leading_combos_dict['Drug 1'] = [c.drug_1 for c in top_combos]
    leading_combos_dict['Drug 2'] = [c.drug_2 for c in top_combos]
    leading_combos_dict['Cell Line'] = [c.CellLine for c in top_combos]

    # setup figure using plotly
    df = pd.DataFrame.from_dict(leading_combos_dict)

    import tempfile
    import webbrowser

    html =  df.to_html()

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        url = 'file://' + f.name
        f.write(html)
    webbrowser.open(url)

    return 
# ================================================================================================================================================================================================================================
def leading_indication_for_combo(combo_id=1):
    # filter combos for a drug, get celline from leading combo
    combo_searched = models.Combo.objects.get(id=combo_id)
    drug_1 = combo_searched.drug_1
    drug_2 = combo_searched.drug_2
    top_combos = models.Combo.objects.filter(
        Q(drug_1__id = drug_1.id) & Q(drug_2__id = drug_2.id) | Q(drug_1__id = drug_2.id) & Q(drug_2__id = drug_1.id),
    ).distinct("Chou_score").order_by("Chou_score", "id")
    # x axis (bins)
    indication_lst = [c.CellLine.indication.cancer_name for c in top_combos]
    # y axis
    chou_score_lst = [c.Chou_score for c in top_combos]

    # setup figure using plotly

    fig = make_subplots()
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))

    # Add traces
    fig.add_trace(
        go.Bar(
            x = indication_lst, 
            y = chou_score_lst, 
            name = "Chou"),
        secondary_y=False,
    )      

    fig.update_layout(
        title={
            'text': 'Leading Indications for Drugs '+drug_1.get_code_name()+" and "+drug_2.get_code_name(),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_title="Chou Scores",
        xaxis_title="Indications",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f",
    ))


    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# =========================================================================================================
def oncolines_heatmap():
    # axes are cell lines v clinically actionable genes, 
    # cell contains IC50 value with color coding for high, medium, and low response (discrete color scale)
    # Check with Mike on specs before building
    
    #discrete color scale normalized between 0-1 (0 being min value and 1 being max value)
    dcolorscale = [
        [0, '#09ffff'],
        [.3, '#09ffff'],
        [.3, '#e763fa'],
        [.7, '#e763fa'],
        [.7, '#ab63fa'],
        [1, '#ab63fa'],
    ] 
    
    # Data
    ic50s = []
    actionable_genes = []
    cell_lines = []

    fig = go.Figure(data=go.Heatmap(
            z=ic50s,
            x=actionable_genes,
            y=cell_lines,
            colorscale=dcolorscale))

    fig.update_layout(
        title='Oncolines data (Heatmap)',
        # xaxis_nticks=36,
        yaxis_title="CellLines",
        xaxis_title="clinically actionable genes",)

    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div
# =========================================================================================================
# APPROVED/COMPLETED GRAPHING FUNCTIONS HERE (USE THESE ONLY:
# =========================================================================================================

def drug_drug_synergy():
    top_combos = models.Combo.objects.order_by('Chou_score')[::-1][2:15]
    dict_out = {}
    dict_out['drug_l']     = [inst.drug_1.drug_name for inst in top_combos]         # x-axis
    dict_out['drug_2']     = [inst.drug_2.drug_name for inst in top_combos]         # x-axis
    dict_out['synergy']     = [inst.Chou_score for inst in top_combos]   # y-axis
    total_avg_chou = np.sum(avg_chou_lst)/len(avg_chou_lst)

    # setup figure using plotly

    fig = make_subplots()
    labels = {'Total Avg Chou': (0,total_avg_chou)}
    line_color = "LightSeaGreen"

    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=14))

    # Add traces
    fig.add_trace(
        go.Bar(
            x = drug_lst, 
            y = avg_chou_lst, 
            name = "Chou"),
        secondary_y=False,
    )


    # Add shapes
    fig.add_trace(
        go.Scatter(
            x = drug_lst,
            y = [total_avg_chou],
            name="Total Avg Chou",
            marker_color = line_color,
            mode = "lines"),
        secondary_y=False,
    )
            
    fig.update_layout(
        title={
            'text': 'Leading Drugs by Chou (w/ Avg)',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"),
        shapes=[
            dict(
            # Line reference to the axes
                type="line",
                yref="y",
                xref= 'paper',
                x0=0,
                y0=total_avg_chou,
                # x1=drug_lst[-1],
                x1=1,
                y1=total_avg_chou,
                line=dict(
                    color=line_color,
                    width=3,
                ),
            )],
        )

    # fig.show()
    plot_div = plot(fig, auto_open=False, output_type = 'div',filename = 'elevations-3d-surface')
    return plot_div