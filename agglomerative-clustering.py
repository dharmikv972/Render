import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
iris=load_iris()
X=iris.data
y=iris.target

Z=linkage(X,'ward')
print(Z)

plt.figure(figsize=(7.5,3.5))
plt.title("IRIS DENDROGRAM")
dendrogram(Z)
plt.show()

model=AgglomerativeClustering(n_clusters=3)
model.fit(X)
labels=model.labels_
print(labels)

plt.figure(figsize=(7.5,3.5))
plt.scatter(X[:,0],X[:,1],c=labels)
plt.xlabel("SEPAL LENGTH")
plt.ylabel("SEPAL WIDTH")
plt.title("AGGLOMERATIVE CLUSTERING RESULTS")
plt.show()
