import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift,estimate_bandwidth
X=np.random.randn(500,2)
print(X)

bandwidth=estimate_bandwidth(X,quantile=0.1,n_samples=100)
print(bandwidth)

ms=MeanShift(bandwidth=bandwidth,bin_seeding=True)
ms.fit(X)

labels=ms.labels_
cluster_centers=ms.cluster_centers_
n_clusters_=len(np.unique(labels))
print("NUMBER OF ESTIMATED CLUSTERS : ",n_clusters_)
plt.figure(figsize=(8,4))
plt.scatter(X[:,0],X[:,1],c=labels,cmap='viridis')
plt.scatter(cluster_centers[:,0],cluster_centers[:,1],marker='*',s=300,c='r')
plt.show()
