from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import pandas as pd

#plt.rcParams["axes.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 7
plt.rcParams["xtick.labelsize"] = 7

data = pd.read_csv(
    './outputs/tags_table.csv', sep="\t", skiprows=1, index_col=0)

#normalise
#data = (data - data.mean()) / data.std()

corr = data.corr()

data_sub = data[data.columns[:5]]

# biplot
#b = sns.pairplot(data_sub, kind='reg', markers="+", diag_kind="kde")

corr_sub_no = 50
corr_sub = corr[corr.columns[:corr_sub_no]][:corr_sub_no]
print(corr_sub)

dn1 = hierarchy.dendrogram(corr_sub)
plt.show()