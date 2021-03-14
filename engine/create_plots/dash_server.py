# Plotly imports
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
import time


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
            value='none',
            clearable=False
        )]),
    dcc.Graph(id='plot'),
    dcc.Loading(
        id="loading-1",
        type="default",
        fullscreen=True,
        children=html.Div(id="loading-output-1")
    )
])

@app.callback(Output("loading-output-1", "children"), Input('analysis-type', 'value'))
def input_triggers_spinner(value):
    time.sleep(1)
    # return ''

@app.callback(Output('plot', 'figure'), Input('analysis-type', 'value'))
def update_plot(analysis_type):
    if analysis_type == 'none':
        return go.Figure()

    elif analysis_type == 'pca_2D':
        # TODO: Replace example data
        df = px.data.iris()
        X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

        pca = PCA(n_components=2)
        components = pca.fit_transform(X)

        fig = px.scatter(components, x=0, y=1, color=df['species'])
        return fig
    
    elif analysis_type == 'pca_3D':
        # TODO: Replace example data
        df = px.data.iris()
        X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

        pca = PCA(n_components=3)
        components = pca.fit_transform(X)

        total_var = pca.explained_variance_ratio_.sum() * 100

        fig = px.scatter_3d(
            components, x=0, y=1, z=2, color=df['species'],
            title=f'Total Explained Variance: {total_var:.2f}%',
            labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
        )
        return fig
    
    elif analysis_type == 'hca_dendrogram':
        X = np.random.rand(15, 12) # 15 samples, with 12 dimensions each
        fig = ff.create_dendrogram(X)
        return fig
    
    elif analysis_type == 'hca_heatmap':
        # TODO: Replace example data
        return go.Figure()
        # get data
        # data = np.genfromtxt("http://files.figshare.com/2133304/ExpRawData_E_TABM_84_A_AFFY_44.tab",
        #                     names=True,usecols=tuple(range(1,30)),dtype=float, delimiter="\t")
        # data_array = data.view((np.float, len(data.dtype.names)))
        # data_array = data_array.transpose()
        # labels = data.dtype.names

        # # Initialize figure by creating upper dendrogram
        # fig = ff.create_dendrogram(data_array, orientation='bottom', labels=labels)
        # for i in range(len(fig['data'])):
        #     fig['data'][i]['yaxis'] = 'y2'

        # # Create Side Dendrogram
        # dendro_side = ff.create_dendrogram(data_array, orientation='right')
        # for i in range(len(dendro_side['data'])):
        #     dendro_side['data'][i]['xaxis'] = 'x2'

        # # Add Side Dendrogram Data to Figure
        # for data in dendro_side['data']:
        #     fig.add_trace(data)

        # # Create Heatmap
        # dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
        # dendro_leaves = list(map(int, dendro_leaves))
        # data_dist = pdist(data_array)
        # heat_data = squareform(data_dist)
        # heat_data = heat_data[dendro_leaves,:]
        # heat_data = heat_data[:,dendro_leaves]

        # heatmap = [
        #     go.Heatmap(
        #         x = dendro_leaves,
        #         y = dendro_leaves,
        #         z = heat_data,
        #         colorscale = 'Blues'
        #     )
        # ]

        # heatmap[0]['x'] = fig['layout']['xaxis']['tickvals']
        # heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

        # # Add Heatmap Data to Figure
        # for data in heatmap:
        #     fig.add_trace(data)

        # # Edit Layout
        # fig.update_layout({'width':800, 'height':800,
        #                         'showlegend':False, 'hovermode': 'closest',
        #                         })
        # # Edit xaxis
        # fig.update_layout(xaxis={'domain': [.15, 1],
        #                                 'mirror': False,
        #                                 'showgrid': False,
        #                                 'showline': False,
        #                                 'zeroline': False,
        #                                 'ticks':""})
        # # Edit xaxis2
        # fig.update_layout(xaxis2={'domain': [0, .15],
        #                                 'mirror': False,
        #                                 'showgrid': False,
        #                                 'showline': False,
        #                                 'zeroline': False,
        #                                 'showticklabels': False,
        #                                 'ticks':""})

        # # Edit yaxis
        # fig.update_layout(yaxis={'domain': [0, .85],
        #                                 'mirror': False,
        #                                 'showgrid': False,
        #                                 'showline': False,
        #                                 'zeroline': False,
        #                                 'showticklabels': False,
        #                                 'ticks': ""
        #                         })
        # # Edit yaxis2
        # fig.update_layout(yaxis2={'domain':[.825, .975],
        #                                 'mirror': False,
        #                                 'showgrid': False,
        #                                 'showline': False,
        #                                 'zeroline': False,
        #                                 'showticklabels': False,
        #                                 'ticks':""})
        # return fig


if __name__ == '__main__':
    app.run_server(debug=True)