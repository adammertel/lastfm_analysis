import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering

data = pd.read_csv(
    './../../data//tags_countries.csv', sep="\t", skiprows=1, index_col=0)
data = data.drop(data.index[0])

clusters = AgglomerativeClustering(n_clusters=6).fit(data)

dists = pdist(data)
links = linkage(pdist(data), 'ward')

#print(len(dists))
out_data = data.loc[:, []]
print(out_data)
out_data.insert(0, '0.30', fcluster(links, 0.30, 'distance'))
out_data.insert(0, '0.25', fcluster(links, 0.25, 'distance'))
out_data.insert(0, '0.20', fcluster(links, 0.20, 'distance'))
out_data.insert(0, '0.15', fcluster(links, 0.15, 'distance'))
out_data.insert(0, '0.10', fcluster(links, 0.10, 'distance'))
out_data.insert(0, '0.05', fcluster(links, 0.05, 'distance'))

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
#plt.show()

out_data.to_csv("./../output/agglomerations.csv", sep="\t")
