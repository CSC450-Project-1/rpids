# _______________________________________________________________________________________________________________________________

#  Project Name:      Response Pattern-Based Identification System (RPIDS)
#  Purpose:           A Graphical User Interface (GUI) based software to assist chemists in performing principal component
#                     analysis (PCA) and hierarchical clustering analysis (HCA).
#  Project Members:   Zeth Copher
#                     Josh Kuhn
#                     Ryan Luer
#                     Austin Pearce
#                     Rich Russell
#  Course:         Missouri State University CSC450 - Intro to Software Engineering Spring 2021
#  Instructor:     Dr. Razib Iqbal, Associate Professor of Computer Science
#  Contact:        RIqbal@MissouriState.edu

#  License:
#  Copyright 2021 Missouri State University

#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sub-license, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:

#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# _______________________________________________________________________________________________________________________________________

# Plotly imports
import pandas as pd
import os
import time
import sys
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash_patch as patch

# Dash imports
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output

# Imports used for Pyinstaller (DO NOT REMOVE)
import sklearn.utils._weight_vector
import sklearn.utils._cython_blas
from sklearn.decomposition import PCA

# HCA imports
import plotly.figure_factory as ff
import numpy as np
from scipy.spatial.distance import pdist, squareform
np.random.seed(1)

temp_path = sys.argv[1]
# external_stylesheets = ['./electron/assets/css/main.css'] NOT WORKING
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
    # Represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.Div(
        id='normalization',
        children=[
            html.Label(['Data Preprocessing']),
            dcc.Dropdown(
                id='normalization-dropdown',
                options=[
                    {'label': 'None', 'value': 'none'},
                    {'label': 'Linear Rescaling', 'value': 'linear_rescaling'},
                    {'label': 'Standardization', 'value': 'standardization'},
                ],
                value='none',
                clearable=False
            )
        ]
    ),
    html.Div(
        id='hca-orientation',
        children=[
            html.Label(['Orientation']),
            dcc.Dropdown(
                id='hca-dropdown',
                options=[
                    {'label': 'Horizontal', 'value': 'horizontal'},
                    {'label': 'Vertical', 'value': 'vertical'},
                ],
                value='horizontal',
                clearable=False
            )
        ]
    ),
    html.Div(
        id='marker-customize',
        children=[
            html.Label(['Marker Size']),
            dcc.Slider(
                id='marker-slider',
                min=1,
                max=10,
                marks={i: format(i) for i in range(1, 11)},
                value=5,
            )
        ]
    ),
    dcc.Graph(id='plot',
              config={
                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                  'displaylogo': False,
                  'toImageButtonOptions': {
                      'format': 'svg',
                      'filename': 'plotly_graph'  # TODO: Can customize filename
                  },
                  'responsive': True,
              },
              figure={
                  'layout': {
                      'autosize': True,
                  }
              },
              style={'flex': '1 1 auto'}),

    dcc.Loading(
        id="loading-1",
        type="default",
        fullscreen=True,
        children=html.Div(id="loading-spinner")
    )
], style={'display': 'flex', 'flex-flow': 'column', 'height': '100vh'})


# ______________________________________________________________
# show_loading function:
# displays the loading spinner
#
# return value:
# return
#
# reference parameters:
# value         n/a         value is a place holder and only acts as a bug preventer
#
# local variables:
# none
# _______________________________________________________________

@app.callback(Output("loading-spinner", "children"), Input('url', 'pathname'))
def show_loading(value):
    time.sleep(1)
    return

# ______________________________________________________________
# showOrientation function:
# This function checks the pathname and passed on the pathname
# the function will display/not display a drop down containing
# the two options for orientation: Horizontal and Vertical.
#
# return value:
# returns the display value as either 'block' or 'none' depending
# on the pathname
#
# reference parameters:
# pathname     string        name of the current path
#
# local variables:
# none
# _______________________________________________________________


@app.callback(Output('hca-orientation', 'style'), Input('url', 'pathname'))
def showOrientation(pathname):
    return {'display': 'block'} if (pathname == '/hca/dendrogram') else {'display': 'none'}

# ______________________________________________________________
# showNormalization function:
# This function checks the pathname and passed on the pathname
# the function will display/not display a drop down containing
# the three options for normalization: None, Linear Rescaling,
# and Standardization.
#
# return value:
# returns the display value as either 'block' or 'none' depending
# on the pathname
#
# reference parameters:
# pathname     string        name of the current path
#
# local variables:
# none
# _______________________________________________________________


# TODO Need to also consider label
@app.callback(Output('normalization-dropdown', 'style'), Input('url', 'pathname'))
def showNormalization(pathname):
    return {'display': 'block'} if (pathname == '/hca/dendrogram' or pathname == '/pca/2d' or pathname == '/pca/3d') else {'display': 'none'}

# ______________________________________________________________
# showMarkerSizing function:
# This function checks the pathname and passed on the pathname
# the function will display/not display a slider to adjust marker
# size.
#
# return value:
# returns the display value as either 'block' or 'none' depending
# on the pathname
#
# reference parameters:
# pathname     string        name of the current path
#
# local variables:
# none
# _______________________________________________________________


@app.callback(Output('marker-customize', 'style'), Input('url', 'pathname'))
def showMarkerSizing(pathname):
    return {'display': 'initial'} if (pathname == '/pca/2d' or pathname == '/pca/3d') else {'display': 'none'}

# ______________________________________________________________
# updatePlot function:
# This function takes the URL routing to display figures accordingly
#
# return value:
# fig                   graph object
#
# reference parameters:
# pathname              string      name of the current path
# normalization_type    string      type of normalization
# hca_orientation       string      orientation of dendrogram
# marker_size           int         size of the marker on slider
#
# local variables:
# fig          graph object
# columns      list                 list of column names from the dataset
# data         pandas dataframe     same dataframe as import but does not have last two
#                                   columns with file names
# _______________________________________________________________


@app.callback(Output('plot', 'figure'),
              Input('url', 'pathname'), Input('normalization-dropdown', 'value'), Input('hca-dropdown', 'value'), Input('marker-slider', 'value'))
def updatePlot(pathname, normalization_type, hca_orientation, marker_size):
    fig = go.Figure()
    if pathname == '/shutdown':
        shutdown()
    elif(os.path.isfile(getDataPath("data.json"))):
        layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)')
        dataset = pd.read_json(getDataPath("data.json"))

        columns = dataset.columns.tolist()
        data = pd.DataFrame.from_dict(dataset)
        data.drop(data.iloc[:, (dataset.columns.size - 2) :dataset.columns.size], inplace=True, axis=1)
        if pathname == '/pca/2d':
            fig = initShowPCA('2D', dataset, data, normalization_type)
            fig = updateMarkerSize(fig, marker_size, layout)
        elif pathname == '/pca/3d':
            fig = initShowPCA('3D', dataset, data, normalization_type)
            fig = updateMarkerSize(fig, marker_size, layout)
        elif pathname == '/hca/dendrogram':
            fig = showHCADendrogram(
                dataset, data, hca_orientation, normalization_type)
        elif pathname == '/hca/heatmap':
            fig = showHCAHeatmap(dataset)
        fig.to_json(getDataPath("data.json"))

    return fig

# ______________________________________________________________
# shutdown function:
# closes down the
#
# return value:
# none
#
# reference parameters:
# none
#
# local variables:
# none
# _______________________________________________________________


def shutdown():
    sys.stderr.close()

# ______________________________________________________________
# initShowPCA function:
# This function normalizes the data before calling the corresponding
# PCA function.
#
# return value:
# showPCA2D/showPCA3D   functions
#
# reference parameters:
# type                  string                specifies 2D or 3D plot
# normalization_type    string                type of normalization
# dataset               pandas dataframe      original dataset
# data                  pandas dataframe      input dataset with no strings
#
# local variables:
# normalized_data       pandas dataframe    dataframe of standardized input data
# _______________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 3.1, 3.2) - Page 4
# Software Design Document (SDD) :                ( functional e,f) - Page 4
# ___________________________________________________________________


def initShowPCA(type, dataset, data, normalization_type):
    if normalization_type == 'linear_rescaling':
        normalized_data = (data-data.min()) / \
            (data.max()-data.min())
    elif normalization_type == 'standardization':
        normalized_data = (data-data.mean())/data.std()
    else:
        normalized_data = pd.DataFrame.from_dict(data)
    return showPCA2D(dataset, normalized_data) if (type == '2D') else showPCA3D(dataset, normalized_data)

# ______________________________________________________________
# showPCA2D function:
# This function displays the 2D PCA plot.
#
# return value:
# fig           graph object
#
# reference parameters:
# none
#
# local variables:
# fig               graph object        current plot object
# pca               ndarray             results of pca calculation
# X                 list                list of samples and run
# components        ndarray             components of normalized data
# eigen_values      list                list of float eigen_values
# eigen_vectors     list                list of float eigen_vectors
# eigen_data        array               array of float eigen_values and eigen_vectors
# compnents_df      pandas dataframe    dataframe of components
# _______________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 4, 5.1) - Page 4
# Software Design Document (SDD) :                ( functional g) - Page 4
# ___________________________________________________________________


def showPCA2D(dataset, normalized_data):
    pca = PCA(n_components=2)
    X = []
    for col in dataset.columns:
        if col != "Samples" and col != "run":
            X.append(col)

    components = pca.fit_transform(normalized_data[X])

    eigen_values = pca.explained_variance_
    eigen_vectors = pca.components_
    fig = px.scatter(components, x=0, y=1,
                     hover_name=dataset["run"], color=dataset["Samples"])
    eigen_values = pca.explained_variance_
    eigen_vectors = pca.components_
    eigen_data = np.array([eigen_values, [eigen_vectors]])
    pd.DataFrame(eigen_data).to_json(getDataPath("eig_data.json"))
    components_df = pd.DataFrame(components)
    components_df["Samples"] = dataset["Samples"].values.tolist()
    components_df["run"] = dataset["run"].values.tolist()
    components_df.to_json(getDataPath("computed_data.json"))

    return fig

# ______________________________________________________________
# showPCA3D function:
# This function displays the 3D PCA plot.
#
# return value:
# fig           graph object
#
# reference parameters:
# none
#
# local variables:
# fig               graph object        current plot object
# pca               ndarray             results of pca calculation
# X                 list                list of samples and run
# components        ndarray             components of normalized data
# total_var         int                 sum of the variances from pca
# eigen_values      list                list of float eigen_values
# eigen_vectors     list                list of float eigen_vectors
# eigen_data        array               array of float eigen_values and eigen_vectors
# compnents_df      pandas dataframe    dataframe of components
# _______________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 4, 5.2) - Page 4
# Software Design Document (SDD) :                ( functional h) - Page 4
# ___________________________________________________________________


def showPCA3D(dataset, normalized_data):
    X = []
    for col in dataset.columns:
        if col != "Samples" and col != "run":
            X.append(col)
    pca = PCA(n_components=3)
    components = pca.fit_transform(normalized_data[X])

    total_var = pca.explained_variance_ratio_.sum() * 100

    fig = px.scatter_3d(
        components, x=0, y=1, z=2, hover_name=dataset["run"], color=dataset["Samples"],
        title=f'Total Explained Variance: {total_var:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'})
    eigen_values = pca.explained_variance_
    eigen_vectors = pca.components_
    eigen_data = np.array([eigen_values, [eigen_vectors]])
    pd.DataFrame(eigen_data).to_json(getDataPath("eig_data.json"))
    components_df = pd.DataFrame(components)
    components_df["Samples"] = dataset["Samples"].values.tolist()
    components_df["run"] = dataset["run"].values.tolist()
    components_df.to_json(getDataPath("computed_data.json"))
    return fig

# ______________________________________________________________
# showHCADendrogram function:
# This function displays the HCA dendrogram.
#
# return value:
# fig                  graph object
#
# reference parameters:
# orientation           string                specifies the orientation of the dendrogram
# normalization_type    string                type of normalization
# dataset               pandas dataframe      original dataset
# data                  pandas dataframe      input dataset with no strings
#
# local variables:
# linear_rescaling      pandas dataframe    dataframe of normalized data
# standardizaiton       pandas dataframe    dataframe of normalized data
# normalized_data       pandas dataframe    dataframe of standardized input data
# label                 list                list of labels
# samples               list                list of sample names
# runs                  list                list of the runs
# fig                   graph object        dendrogram plot
# _______________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 3, 6, 7, 7.2) - Pages 4,6,7
# Software Design Document (SDD) :                ( functional e,f,k) - Page 5
# ___________________________________________________________________


def showHCADendrogram(dataset, data, orientation, normalization_type):
    if normalization_type == 'linear_rescaling':
        linear_rescaling = (data-data.min()) / \
            (data.max()-data.min())
        normalized_data = linear_rescaling.iloc[:, [3, 4]].values
    elif normalization_type == 'standardization':
        standardization = (data-data.mean())/data.std()
        normalized_data = standardization.iloc[:, [3, 4]].values
    else:
        normalized_data = data.iloc[:, [3, 4]].values

    label = []
    samples = dataset["Samples"].tolist()
    runs = dataset["run"].tolist()
    for i in range(dataset["Samples"].size):
        if len(runs[i] + samples[i]) >= 25:
            nL = samples[i] + " " + runs[i]
            label.append(nL[:15:])
        else:
            label.append(samples[i] + " " + runs[i])
    if orientation == 'horizontal':
        fig = ff.create_dendrogram(
            normalized_data, orientation='left', labels=label)
        if len(dataset.index) > 20 and dataset.columns.size < 20:
            fig.update_layout(width=1500, height=900)
        elif len(dataset.index) < 20 and dataset.columns.size < 20:
            fig.update_layout(width=1500, height=900)
    elif orientation == 'vertical':
        fig = ff.create_dendrogram(normalized_data, labels=label)
        if len(dataset.index) > 25 and dataset.columns.size < 20:
            fig.update_layout(width=1500, height=900)
        elif len(dataset.index) < 25 and dataset.columns.size < 20:
            fig.update_layout(width=1500, height=900)
    return fig

# ______________________________________________________________
# showHCAHeatmap function:
# This function displays the HCA heatmap.
#
# return value:
# fig
#
# reference parameters:
# dataset               pandas dataframe      original imported dataset
# 
# local variables:
# label                 list                list of labels
# samples               list                list of sample names
# runs                  list                list of the runs
# fig                   graph object        top dendrogram for heatmap
# df                    pandas dataframe    imported data without the run and Samples columns
# dendro_sides          graph object        side dendrogram for heatmap
# dendro_leaves         list                list of dendro_sides
# heat_data             list                list of heatmap data
# heatmap               graph object        heatmap plot
# _______________________________________________________________
#
# The code block below fulfills the requirements of:
#
# Software Requirement Specification (SRS):    ( functional 6, 7, 7.1) - Page 6,7
# Software Design Document (SDD) :                ( functional l) - Page x
# ___________________________________________________________________


def showHCAHeatmap(dataset):
    label = []
    samples = dataset["Samples"].tolist()
    runs = dataset["run"].tolist()
    for i in range(dataset["Samples"].size):
        if len(runs[i] + samples[i]) >= 25:
            nL = samples[i] + " " + runs[i]
            label.append(nL[:15:])
        else:
            label.append(samples[i] + " " + runs[i])
    df = dataset.drop('Samples', axis=1)
    df = df.drop('run', axis=1)
    fig = ff.create_dendrogram(
        df, orientation='bottom', labels=label)
    for i in range(len(fig['data'])):
        fig['data'][i]['yaxis'] = 'y2'

    dendro_side = ff.create_dendrogram(
        df, orientation='right')
    for i in range(len(dendro_side['data'])):
        dendro_side['data'][i]['xaxis'] = 'x2'

    for data in dendro_side['data']:
        fig.add_trace(data)

    dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    dendro_leaves = list(map(int, dendro_leaves))
    data_dist = pdist(df)
    heat_data = squareform(data_dist)
    heat_data = heat_data[dendro_leaves, :]
    heat_data = heat_data[:, dendro_leaves]

    heatmap = [
        go.Heatmap(
            x=dendro_leaves,
            y=dendro_leaves,
            z=heat_data,
            colorscale='Blues'
        )
    ]

    heatmap[0]['x'] = fig['layout']['xaxis']['tickvals']
    heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    for data in heatmap:
        fig.add_trace(data)
    if len(dataset.index) > 20 and dataset.columns.size < 20:
        fig.update_layout(width=1200, height=1000)
    elif len(dataset.index) < 20 and dataset.columns.size < 20:
        fig.update_layout(width=1200, height=1000)
    fig.update_layout({'showlegend': False, 'hovermode': 'closest'})

    fig.update_layout(xaxis={'domain': [.15, 1],
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'ticks': ""})

    fig.update_layout(xaxis2={'domain': [0, .15],
                              'mirror': False,
                              'showgrid': False,
                              'showline': False,
                              'zeroline': False,
                              'showticklabels': False,
                              'ticks': ""})

    fig.update_layout(yaxis={'domain': [0, .85],
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'showticklabels': False,
                             'ticks': ""
                             })

    fig.update_layout(yaxis2={'domain': [.825, .975],
                              'mirror': False,
                              'showgrid': False,
                              'showline': False,
                              'zeroline': False,
                              'showticklabels': False,
                              'ticks': ""})
    return fig

# ______________________________________________________________
# updateMarkerSize function:
# This function allows for customizing the marker size
#
# return value:
# fig           graph object
#
# reference parameters:
# fig           graph object    current plot object
# marker_size   int             marker size number
# layout        string          string of the current layout
#
# local variables:
# none
# _______________________________________________________________


def updateMarkerSize(fig, marker_size, layout):
    fig.update_traces(marker=dict(
        size=marker_size
    )
    )

    fig.update_layout(layout)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray',
                     zeroline=True, zerolinewidth=2, zerolinecolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray',
                     zeroline=True, zerolinewidth=2, zerolinecolor='LightGray')
    return fig

# ______________________________________________________________
# getDataPath function:
# This function grabs the data path
#
# return value:
# os.path.join(temp_path, filename)     operating system path join
#
# reference parameters:
# filename          string      string of the filename
#
# local variables:
# none
# _______________________________________________________________


def getDataPath(filename):
    return os.path.join(temp_path, filename)

# ______________________________________________________________
# isDev function:
# This function grabs the data path
#
# return value:
# boolean
#
# reference parameters:
# none
#
# local variables:
# CURR_DIR          string         name of the directory
# folder_name       string         name of the folder
# _______________________________________________________________


def isDev():
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    folder_name = os.path.basename(CURR_DIR)
    return True if(folder_name == 'engine') else False


if __name__ == '__main__':
    app.run_server(debug=isDev())
