# Plotly imports
import time
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# PCA imports
from sklearn.decomposition import PCA

# HCA imports
import plotly.figure_factory as ff
import numpy as np
from scipy.spatial.distance import pdist, squareform
np.random.seed(1)

# Misc imports
app = dash.Dash()
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='analysis-type',
            options=[
                {'label': 'Please select a type of analysis', 'value': 'none'},
                {'label': 'PCA 2D', 'value': 'pca_2D'},
                {'label': 'PCA 3D', 'value': 'pca_3D'},
                {'label': 'HCA Dendrogram', 'value': 'hca_dendrogram'},
                {'label': 'HCA Heatmap', 'value': 'hca_heatmap'}
            ],
            value='pca_2D',  # TODO
            clearable=False
        )]),
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
                  }
              }),
    dcc.Loading(
        id="loading-1",
        type="default",
        fullscreen=True,
        children=html.Div(id="loading-spinner")
    )
])

# Show loading spinner


@app.callback(Output("loading-spinner", "children"), Input('analysis-type', 'value'))
def show_loading(value):
    time.sleep(1)
    return

# Show/hide HCA dropdown


@app.callback(Output('hca-orientation', 'style'), Input('analysis-type', 'value'))
def show_hca_dropdown(analysis_type):
    if analysis_type == 'hca_dendrogram':
        return {'visibility': 'visible'}
    else:
        return {'visibility': 'hidden'}

# Return selected plot type


@app.callback(Output('plot', 'figure'), Input('analysis-type', 'value'), Input('normalization-dropdown', 'value'), Input('hca-dropdown', 'value'), Input('marker-slider', 'value'))
def update_plot(analysis_type, normalization_type, hca_orientation, marker_size):

    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')

    dataset = pd.read_json("./temp/data.json", orient="", typ="frame")
    columns = dataset.columns.tolist()

    if(analysis_type == 'hca_dendrogram'):
        if normalization_type == 'linear_rescaling':
            linear_rescaling = (dataset-dataset.min()) / \
                (dataset.max()-dataset.min())
            X = linear_rescaling.iloc[:, [3, 4]].values
        elif normalization_type == 'standardization':
            standardization = (dataset-dataset.mean())/dataset.std()
            X = standardization.iloc[:, [3, 4]].values
        else:
            X = dataset.iloc[:, [3, 4]].values

    elif(analysis_type == 'pca_2D' or analysis_type == 'pca_3D'):
        if normalization_type == 'linear_rescaling':
            linear_rescaling = (dataset-dataset.min()) / \
                (dataset.max()-dataset.min())
            X = linear_rescaling[columns]
        elif normalization_type == 'standardization':
            standardization = (dataset-dataset.mean())/dataset.std()
            X = standardization[columns]
        else:
            col_list = dataset[columns]

    if analysis_type == 'none':
        fig = go.Figure()

    elif analysis_type == 'pca_2D':
        pca = PCA(n_components=2)
        #X = ["H2O", " Ni(II)", " Cu(II)", " Fe(II)", " Fe(III) "]
        components = pca.fit_transform(dataset[columns])

        fig = px.scatter(components, x=0, y=1, color=0)

    elif analysis_type == 'pca_3D':
        pca = PCA(n_components=3)
        components = pca.fit_transform(X)

        total_var = pca.explained_variance_ratio_.sum() * 100

        fig = px.scatter_3d(
            components, x=0, y=1, z=2, color=columns,
            title=f'Total Explained Variance: {total_var:.2f}%',
            labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
        )

    elif analysis_type == 'hca_dendrogram':
        if hca_orientation == 'horizontal':
            fig = ff.create_dendrogram(X, orientation='right')
        elif hca_orientation == 'vertical':
            fig = ff.create_dendrogram(X)

    elif analysis_type == 'hca_heatmap':
        fig = px.imshow(dataset)
        return fig

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

    fig.to_json('./temp/data.json')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
