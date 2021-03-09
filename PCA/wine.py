from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from matplotlib.colors import ListedColormap


dataset = pd.read_csv('wine.csv')

dataset.head()

# split into dependant and independent variable

x = dataset.iloc[:, 0:13].values

y = dataset.iloc[:, 13].values


# splitting dataset into a training set and test set


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=0)


sc = StandardScaler()

x_train = sc.fit_transform(x_train)

x_test = sc.transform(x_test)


pca = PCA(n_components=2)

x_train = sc.fit_transform(x_train)

x_test = sc.transform(x_test)

#explained_variance = pca.explained_variance_ratio


# fitting logistic Regression to training set


classifier = LogisticRegression(random_state=0)

classifier.fit(x_train, y_train)


# predicting results

y_pred = classifier.predict(x_test)

print("accuracy score:", accuracy_score(y_test, y_pred))


# visualising the Training set results

X_set, y_set = x_test, y_test


x1, x2 = np.meshgrid(np.arange(start=X_set[:, 0].min() - 1,
                               stop=X_set[:, 0].max() + 1,
                               step=0.01),
                     np.arange(start=X_set[:, 1].min() - 1,
                               stop=X_set[:, 0].max() + 1,
                               step=0.01))
print(x1, x2)

plt.contourf(x1, x2, classifier.predict

             (np.array([x1.ravel(), x2.ravel()]).reshape(x1.shape),

              alpha=0.75, Cmap=ListedColormap(('red', 'green'))))


plt.xlim(x1.min(), x1.max())

plt.ylim(x1.min(), x1.max())


for i, j in enumerate(np.unique(y_set)):

    plt. scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],

                 c=ListedColormap(('red', 'green', 'blue'))(i), label=j)


plt.title('PCA using Logistic Regression (Training set)')

plt.xlabel('PC1')

plt.ylabel('PC2')

plt.legend()

plt.show()
