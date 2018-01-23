import numpy as np
import pandas as pd
from numpy import genfromtxt
from sklearn.decomposition import PCA

#data = genfromtxt('tags_table.csv', delimiter='\t', skip_header=3)
data = pd.read_csv('tags_table.csv', sep="\t", skiprows=1, index_col=0)
#data = data.drop(data.columns[[0]], axis=1)
data = data.drop(data.index[0])

#data = np.array(tags_data)
#data = np.delete(data, [0, 0], axis=1)

pca = PCA(n_components=6, svd_solver="full")
pca2 = pca.fit(data)
print(pca2.explained_variance_ratio_)
print(pca2.singular_values_)
comps = pca2.components_

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

data.to_csv("outputs/pca.csv", sep="\t")
