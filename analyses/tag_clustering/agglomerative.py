import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering

data = pd.read_csv(
    './../../data//tags_countries.csv', sep="\t", skiprows=1, index_col=0)
data = data.drop(data.index[0])

clusters = AgglomerativeClustering(n_clusters=6).fit(data)

dists = pdist(data)
links = linkage(pdist(data), 'ward')
#print(dists)
#print(len(dists))

plt.figure(figsize=(25, 10))
plt.subplots_adjust(bottom=0.3)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    links,
    color_threshold=0.05,
    leaf_rotation=90,
    leaf_font_size=12,
    labels=data.index)
plt.show()