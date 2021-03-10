import plotly.express as px
from sklearn.decomposition import PCA
import plotly.io as pio
import os
pio.renderers.default = "iframe"


# TODO: SHOW IFRAME
# TODO: READ FROM JSON

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

path = os.path.join(os.path.dirname(os.path.dirname( __file__ )), 'electron', 'iframe_figures')
fig.write_html(os.path.join(path, 'pca_3D.html'))