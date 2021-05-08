
# Plotly imports
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

# Misc imports
import sys
import time
import os
import pandas as pd

temp_path = sys.argv[1]
external_stylesheets = ['./electron/assets/css/main.css']

app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div([
    # Represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.Div(
        id='normalization',
        children=dcc.Dropdown(
            id='normalization-dropdown',
            options=[
                {'label': 'None', 'value': 'none'},
                {'label': 'Linear Rescaling', 'value': 'linear_rescaling'},
                {'label': 'Standardization', 'value': 'standardization'},
            ],
            value='none',
            clearable=False
        )),
    html.Div(
        id='hca-orientation',
        children=dcc.Dropdown(
            id='hca-dropdown',
            options=[
                {'label': 'Horizontal', 'value': 'horizontal'},
                {'label': 'Vertical', 'value': 'vertical'},
            ],
            value='horizontal',
            clearable=False
        )),
    html.Div(
        id='marker-customize',
        children=dcc.Slider(
            id='marker-slider',
            min=1,
            max=10,
            marks={i: format(i) for i in range(1, 11)},
            value=5,
        )
    ),
    dcc.Graph(id='plot',
              config={
                  # TODO: Need to ask Yoshimatsu what he wants
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


# Show loading spinner
@app.callback(Output("loading-spinner", "children"), Input('url', 'pathname'))
def show_loading(value):
    time.sleep(1)
    return

# Show/hide orientation dropdown


@app.callback(Output('hca-orientation', 'style'), Input('url', 'pathname'))
def showOrientation(pathname):
    return {'display': 'block'} if (pathname == '/hca/dendrogram') else {'display': 'none'}

# Show/hide normalization dropdown


@app.callback(Output('normalization-dropdown', 'style'), Input('url', 'pathname'))
def showNormalization(pathname):
    return {'display': 'block'} if (pathname == '/hca/dendrogram' or pathname == '/pca/2d' or pathname == '/pca/3d') else {'display': 'none'}

# Show/hide marker sizing


@app.callback(Output('marker-customize', 'style'), Input('url', 'pathname'))
def showMarkerSizing(pathname):
    return {'display': 'initial'} if (pathname == '/pca/2d' or pathname == '/pca/3d') else {'display': 'none'}

# Use URL routing to show different plots


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
        data.drop(data.iloc[:, (dataset.columns.size - 2):dataset.columns.size], inplace=True, axis=1)
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


def shutdown():
    sys.stderr.close()


def initShowPCA(type, dataset, data, normalization_type):
    if normalization_type == 'linear_rescaling':
        normalized_data = (data-data.min()) / \
            (data.max()-data.min())
    elif normalization_type == 'standardization':
        normalized_data = (data-data.mean())/data.std()
    else:
        normalized_data = pd.DataFrame.from_dict(data)
    return showPCA2D(dataset, normalized_data) if (type == '2D') else showPCA3D(dataset, normalized_data)


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

    # with open(, "w") as outfile:
    #     json_object = json.dumps(json_eig, indent = 4)
    #     outfile.write(json_object)
    return fig


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
        # if dataset.columns.size > 20:
        #     fig.update_layout(width = 4000, height = 4000)
        if len(dataset.index) > 20 and dataset.columns.size < 20:
            fig.update_layout(width = 1500, height = 900)
        elif len(dataset.index) < 20 and dataset.columns.size < 20:
            fig.update_layout(width = 1500, height = 900)
    elif orientation == 'vertical':
        fig = ff.create_dendrogram(normalized_data, labels=label)
        # if dataset.columns.size > 20:
        #     fig.update_layout(width = 4000, height = 4000)
        if len(dataset.index) > 25 and dataset.columns.size < 20:
            fig.update_layout(width = 1500, height = 900)
        elif len(dataset.index) < 25 and dataset.columns.size < 20:
            fig.update_layout(width = 1500, height = 900)
    return fig


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
    # if dataset.columns.size > 20:
    #     fig.update_layout(width = 1700, height = 1500)
    if len(dataset.index) > 20 and dataset.columns.size < 20:
        fig.update_layout(width = 1200, height = 1000)
    elif len(dataset.index) < 20 and dataset.columns.size < 20:
        fig.update_layout(width = 1200, height = 1000)
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


def updateMarkerSize(fig, marker_size, layout):
    # Customize marker size
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

def getDataPath(filename):
    return os.path.join(temp_path, filename)

def isDev():
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    folder_name = os.path.basename(CURR_DIR)
    return True if(folder_name=='engine') else False

if __name__ == '__main__':
    app.run_server(debug=isDev())