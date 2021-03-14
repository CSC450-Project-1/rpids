import plotly.figure_factory as ff
import numpy as np
np.random.seed(1)
import plotly.io as pio
import os
pio.renderers.default = "iframe"


X = np.random.rand(15, 12) # 15 samples, with 12 dimensions each
fig = ff.create_dendrogram(X)
fig.update_layout(width=800, height=500)
path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname( __file__ ))), 'electron', 'iframe_figures')
fig.write_html(os.path.join(path, 'hca_dendrogram.html'))