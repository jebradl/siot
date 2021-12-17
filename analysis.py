import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm

df = pd.read_csv('combined_data.csv') # open datasheet as data frame
df = df.drop('Unnamed: 0', 1) # remove index column

print(df.describe().T) # prints details about the data including mean, variance etc for values

cm = df.corr() # build confusion matrix for df
ax = sns.heatmap(cm, annot=True, square=True, linewidths=.5) # generate heatmap for correlation data
plt.yticks(rotation=0)
plt.xticks(rotation=90) # add labels as appropriate

plt.show()