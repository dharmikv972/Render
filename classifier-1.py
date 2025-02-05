import pandas as pd
import matplotlib.pyplot as plt
fruits=pd.read_table('fruit_data_with_colors.txt')
print(fruits.head())

print(fruits.shape)

print(fruits['fruit_name'].unique())

print(fruits.groupby('fruit_name').size())

import seaborn as sns
sns.countplot(fruits['fruit_name'],label="Count")
plt.show()

fruits.drop('fruit_label',axis=1).plot(kind='box',subplots=True,layout=(2,2),sharex=False,sharey=False,figsize=(9,9),title="BOX PLOT FOR EACH INPUT VARIABLE")
plt.savefig('fruit_box')
plt.show()

import pylab as pl
fruits.drop('fruit_label',axis=1).hist(bins=30,figsize=(9,9))
pl.suptitle("Histogram For Each Nmumeric Input Variable")
pl.savefig('fruits_hist')
plt.show()

print("STATISTICAL SUMMARY")
print(fruits.describe())
