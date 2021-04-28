# Plotly imports
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Dash imports
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash

# Misc imports
from sklearn.decomposition import PCA
import pandas as pd
import os
import time
import numpy as np 
import json

# HCA imports
import numpy as np
from scipy.spatial.distance import pdist, squareform
np.random.seed(1)

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
            value='none',  # TODO
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


@app.callback(Output('normalization-dropdown', 'style'), Input('analysis-type', 'value'))
def show_normalization_dropdown(analysis_type):
    if analysis_type == 'hca_dendrogram' or analysis_type == 'pca_2D' or analysis_type == 'pca_3D':
        return {'visibility': 'visible'}
    else:
        return {'visibility': 'hidden'}


@app.callback(Output('plot', 'figure'), Input('analysis-type', 'value'), Input('normalization-dropdown', 'value'), Input('hca-dropdown', 'value'), Input('marker-slider', 'value'))
def update_plot(analysis_type, normalization_type, hca_orientation, marker_size):
    if(os.path.isfile("./temp/data.json")):
        layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')
        dataset = pd.read_json("./temp/data.json")

        columns = dataset.columns.tolist()

        data = pd.DataFrame.from_dict(dataset)
        data.drop(data.iloc[:, (dataset.columns.size - 2):dataset.columns.size], inplace=True, axis=1)

        if analysis_type == 'none':
            fig = go.Figure()

        if(analysis_type == 'hca_dendrogram'):
            if normalization_type == 'linear_rescaling':
                linear_rescaling = (data-data.min()) / \
                    (data.max()-data.min())
                normalized_data = linear_rescaling.iloc[:, [3, 4]].values
            elif normalization_type == 'standardization':
                standardization = (data-data.mean())/data.std()
                normalized_data = standardization.iloc[:, [3, 4]].values
            else:
                normalized_data = data.iloc[:, [3, 4]].values

        elif(analysis_type == 'pca_2D' or analysis_type == 'pca_3D'):
            if normalization_type == 'linear_rescaling':
                normalized_data = (data-data.min()) / \
                    (data.max()-data.min())
            elif normalization_type == 'standardization':
                normalized_data = (data-data.mean())/data.std()
            else:
                normalized_data = pd.DataFrame.from_dict(data)

        if analysis_type == 'pca_2D':
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
            pd.DataFrame(eigen_data).to_json("./temp/eig_data.json")
            components_df = pd.DataFrame(components)
            components_df["Samples"] = dataset["Samples"].values.tolist()
            components_df["run"] = dataset["run"].values.tolist()
            components_df.to_json("./temp/computed_data.json")
            
            # with open(, "w") as outfile:
            #     json_object = json.dumps(json_eig, indent = 4)
            #     outfile.write(json_object)
        elif analysis_type == 'pca_3D':
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
            pd.DataFrame(eigen_data).to_json("./temp/eig_data.json")
            components_df = pd.DataFrame(components)
            components_df["Samples"] = dataset["Samples"].values.tolist()
            components_df["run"] = dataset["run"].values.tolist()
            components_df.to_json("./temp/computed_data.json")
        elif analysis_type == 'hca_dendrogram':
            label = []
            samples = dataset["Samples"].tolist()
            runs = dataset["run"].tolist()
            for i in range(dataset["Samples"].size):
                label.append(samples[i] + " " + runs[i])
            if hca_orientation == 'horizontal':
                fig = ff.create_dendrogram(
                    normalized_data, orientation='left', labels=label)
                if dataset.columns.size > 20:
                    fig.update_layout(width=1750, height=4000)
            elif hca_orientation == 'vertical':
                fig = ff.create_dendrogram(normalized_data, labels=label)
                if dataset.columns.size > 20:
                    fig.update_layout(width=4000, height=1750)

        elif analysis_type == 'hca_heatmap':
            label = []
            samples = dataset["Samples"].tolist()
            runs = dataset["run"].tolist()
            for i in range(dataset["Samples"].size):
                label.append(samples[i] + " " + runs[i])
            df = dataset.drop('Samples', axis=1)
            df = df.drop('run', axis=1)
            data_array = df.values
            data_array = data_array.transpose()
            fig = ff.create_dendrogram(
                data_array, orientation='bottom', labels=label)
            for i in range(len(fig['data'])):
                fig['data'][i]['yaxis'] = 'y2'

            dendro_side = ff.create_dendrogram(
                data_array, orientation='right')
            for i in range(len(dendro_side['data'])):
                dendro_side['data'][i]['xaxis'] = 'x2'

            for data in dendro_side['data']:
                fig.add_trace(data)

            dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
            dendro_leaves = list(map(int, dendro_leaves))
            data_dist = pdist(data_array)
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

            fig.update_layout({'width': 1200, 'height': 1200,
                               'showlegend': False, 'hovermode': 'closest',
                               })

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
    else:
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)
