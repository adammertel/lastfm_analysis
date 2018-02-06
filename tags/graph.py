import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

data = pd.read_csv(
    './outputs/tags_table.csv', sep="\t", skiprows=1, index_col=0)

#normalise
#data = (data - data.mean()) / data.std()

corr = data.corr()

data_sub = data[data.columns[:5]]

# biplot
#b = sns.pairplot(data_sub, kind='reg', markers="+", diag_kind="kde")

corr_sub_no = 100
corr_sub = corr[corr.columns[:corr_sub_no]][:corr_sub_no]
''' 
links = corr_sub.stack().reset_index()
links['weight'] += 1
links['weight'] /= 2
links.columns = ['source', 'target', 'weight']
links_filtered = links.loc[(links['weight'] > 0)
                           & (links['source'] != links['target'])]
 '''
G = nx.Graph()

added = []
for col in corr_sub.columns:
    for row in corr_sub.index:
        if row != col and col + '-' + row not in added:
            w = (corr_sub[col][row] + 1) / 2
            print w
            added.append(col + '-' + row)
            G.add_edge(col, row, w=float(w))

        #for link in links[column]:
    #print link

#G = nx.from_pandas_edgelist(links_filtered, 'source', 'target', ['weight'])
#print(G)

thresh = 0.7
edges = [(u, v) for (u, v, d) in G.edges(data=True) if d['w'] > thresh]

pos = nx.spectral_layout(G, weight="w")
nx.draw_networkx_nodes(G, pos, node_size=0)
weights = [10 * (G[u][v]['w'] - thresh) for u, v in edges]

nx.draw_networkx_edges(
    G, pos, edgelist=edges, width=weights, alpha=0.6, edge_color='k')

# labels
nx.draw_networkx_labels(
    G,
    pos,
    font_size=11,
    font_color='r',
    font_family='sans-serif',
    font_weigh='bold')

plt.axis('off')
#plt.savefig("weighted_graph.png")  # save as png
plt.show()  # display
