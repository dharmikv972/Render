import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

X,y=load_iris(return_X_y=True)
print(X)
print(y)

sse=[]
for k in range(1, 11):
    km=KMeans(n_clusters=k, random_state=2)
    km.fit(X)
    sse.append(km.inertia_)
sns.set_style("whitegrid")
g=sns.lineplot(x=range(1, 11),y=sse)
g.set(xlabel="NUMBER OF CLUSTERN (K)",
      ylabel="SUM SQUARED ERROR",
      title="ELBOW METHOD")
plt.show()

kmeans=KMeans(n_clusters=3, random_state=2)
kmeans.fit(X)
print(kmeans)

kmeans.cluster_centers_
pred=kmeans.fit_predict(X)
print(pred)

plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.scatter(X[:,0],X[:,1],c=pred,cmap=cm.Accent)
plt.grid(True)
for center in kmeans.cluster_centers_:
    center=center[:2]
plt.scatter(center[0],center[1],marker='^',c='red')
plt.xlabel("PETAL LENGTH (CM)")
plt.ylabel("PETAL WIDTH (CM)")
plt.subplot(1,2,2)
plt.scatter(X[:,2],X[:,3],c=pred,cmap=cm.Accent)
plt.grid(True)
for center in kmeans.cluster_centers_:
    center=center[2:4]
plt.scatter(center[0],center[1],marker='^',c='red')
plt.xlabel("SEPAL LENGTH (CM)")
plt.ylabel("SEPAL WIDTH (CM)")
plt.show()
