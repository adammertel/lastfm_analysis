import numpy as np
import pandas as pd
from numpy import genfromtxt
import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import seaborn as sns

#plt.rcParams["axes.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 7
plt.rcParams["xtick.labelsize"] = 7

data = pd.read_csv(
    './outputs/tags_table.csv', sep="\t", skiprows=1, index_col=0)

data = data.drop(data.index[0])

#normalise
#data = (data - data.mean()) / data.std()

corr = data.corr()
corr.to_csv("outputs/tags_corr.csv", sep="\t")

data_sub = data[data.columns[:5]]

# biplot
#b = sns.pairplot(data_sub, kind='reg', markers="+", diag_kind="kde")

corr_sub_no = 50
corr_sub = corr[corr.columns[:corr_sub_no]][:corr_sub_no]
print(corr_sub)
sns.clustermap(corr_sub, cmap="PiYG", vmin=-1, vmax=1)

plt.show()
''' plt.matshow(corr, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1)
plt.xticks(range(len(data.columns)), data.columns, rotation=90)
plt.yticks(range(len(data.columns)), data.columns)
plt.colorbar()
plt.show() '''