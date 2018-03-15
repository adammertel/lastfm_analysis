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

data_f = data.copy()

# removing tags with big portion of 0 values
for column in data:
    if 0.0000 in data[column].value_counts():
        if data[column].value_counts()[0] * 100 / len(data) > 50:
            data_f.drop(column, axis=1, inplace=True)

#print data_f

#normalise
#data = (data - data.mean()) / data.std()

corr = data_f.corr()
corr.to_csv("outputs/tags_corr.csv", sep="\t")

corr_plus = corr[corr > 0.5]
corr_plus = corr_plus[corr_plus != 1]
corr_plus = (corr_plus - 0.5) * 2
corr_plus.fillna(value=0, inplace=True)
corr_plus.to_csv("outputs/tags_corr_plus.csv", sep="\t")

# biplot
#b = sns.pairplot(data_sub, kind='reg', markers="+", diag_kind="kde")
corr_sub_no = 50
corr_sub = corr[corr.columns[:corr_sub_no]][:corr_sub_no]
#print(corr_sub)
sns.clustermap(corr_sub, cmap="PiYG", vmin=-1, vmax=1)

# countries
corr_c = data.T.corr()
corr_c.to_csv("outputs/countries_corr.csv", sep="\t")

corr_c_plus = corr_c[corr_c > 0.99]
corr_c_plus = corr_c_plus[corr_c_plus != 1]
corr_c_plus = (corr_c_plus - 0.99) * 100
corr_c_plus.fillna(value=0, inplace=True)
corr_c_plus.to_csv("outputs/countries_corr_plus.csv", sep="\t")

#plt.show()
''' plt.matshow(corr, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1)
plt.xticks(range(len(data.columns)), data.columns, rotation=90)
plt.yticks(range(len(data.columns)), data.columns)
plt.colorbar()
plt.show() '''
