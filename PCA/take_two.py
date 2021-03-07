
import numpy as np
import pandas as pd
from sklearn import datasets
import matplotlib.pyplot as plt

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# load dataset into Pandas DataFrame
df = pd.read_csv(url, names=['sepal length', 'sepal width',
                             'petal length', 'petal width', 'target'])
