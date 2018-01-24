import numpy as np
import pandas as pd
from numpy import genfromtxt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift, estimate_bandwidth

import matplotlib.pyplot as plt
from itertools import cycle

#data = genfromtxt('tags_table.csv', delimiter='\t', skip_header=3)
data = pd.read_csv(
    './outputs/tags_table.csv', sep="\t", skiprows=1, index_col=0)
#data = data.drop(data.columns[[0]], axis=1)
data = data.drop(data.index[0])

#data = np.array(tags_data)
#data = np.delete(data, [0, 0], axis=1)

# normalise
data = (data - data.mean()) / data.std()
#data = (data-df.min())/(data.max()-data.min())
data.to_csv("outputs/pca_n.csv", sep="\t")

pca = PCA(n_components=2, svd_solver="full").fit(data)
data_t = pca.transform(data)

# k means clustering
np.savetxt("outputs/pca_t.csv", data_t, delimiter="\t")

clusters_kmeans = KMeans(n_clusters=4, random_state=0).fit(data_t)

# mean shift clustering
bandwidth = estimate_bandwidth(data_t, quantile=0.12, n_samples=200)
clusters_ms = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(data_t)

groups_kmean = clusters_kmeans.labels_
groups_ms = clusters_ms.labels_

print(clusters_ms.labels_)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)
comps = pca.components_

for ci, comp in enumerate(comps):
    PC_row = pd.DataFrame([comp], columns=list(data.columns.values))
    PC_row = PC_row.rename({0: 'PCA' + str(ci + 1)})
    data = data.append(PC_row)

comps_vals = []
for ci, comp in enumerate(comps):
    comp_vals = []
    for ri, row in data.iterrows():
        country_comp_val = 0
        for ti, tag_val in enumerate(row):
            country_comp_val += tag_val * comp[ti]
        comp_vals.append(country_comp_val)

    comps_vals.append(comp_vals)

for ci, comp in enumerate(comps):
    data['PC' + str(ci + 1) + '_sum'] = comps_vals[ci]

data['clusters_kmeans'] = np.append(groups_kmean, [0] * len(comps))
data['clusters_ms'] = np.append(groups_ms, [0] * len(comps))

data.to_csv("outputs/pca.csv", sep="\t")

# plotting mean shift
''' labels = clusters_ms.labels_
cluster_centers = clusters_ms.cluster_centers_
labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    print(data_t)

    plt.plot(data_t[my_members, 0], data_t[my_members, 1], col + '.')
    plt.plot(
        cluster_center[0],
        cluster_center[1],
        'o',
        markerfacecolor=col,
        markeredgecolor='k',
        markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show() '''
