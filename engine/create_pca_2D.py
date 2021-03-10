import plotly.express as px
from sklearn.decomposition import PCA
import plotly.io as pio
import os
pio.renderers.default = "iframe"

df = px.data.iris()
X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]

pca = PCA(n_components=2)
components = pca.fit_transform(X)

fig = px.scatter(components, x=0, y=1, color=df['species'])
path = os.path.join(os.path.dirname(os.path.dirname( __file__ )), 'electron', 'iframe_figures')
fig.write_html(os.path.join(path, 'pca_2D.html'))