import pandas as pd 
import numpy as np
import math
import re
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from surprise import Dataset,SVD,Reader
from surprise.model_selection import cross_validate
sns.set_style("darkgrid")
import os
from pathlib import Path
from datetime import datetime

print('Start analisys {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) )
print('Current directory: ' + os.getcwd())
df1 = pd.read_csv('archive/combined_data_4.txt', header= None,names= ['user_id', 'Rating'],usecols = [0,1])

df1['Rating'] = df1['Rating'].astype(float)

print('Dataset 1 shape : {}'.format(df1.shape))
print('Dataset examples-')
print(df1.loc[::5000000,:])

df = df1

"""

df2 = pd.read_csv('archive/combined_data_2.txt', header = None, names = ['Cust_Id', 'Rating'], usecols = [0,1])
df3 = pd.read_csv('archive/combined_data_3.txt', header = None, names = ['Cust_Id', 'Rating'], usecols = [0,1])
df4 = pd.read_csv('archive/combined_data_4.txt', header = None, names = ['Cust_Id', 'Rating'], usecols = [0,1])


df2['Rating'] = df2['Rating'].astype(float)
df3['Rating'] = df3['Rating'].astype(float)
df4['Rating'] = df4['Rating'].astype(float)

print('Dataset 2 shape: {}'.format(df2.shape))
print('Dataset 3 shape: {}'.format(df3.shape))
print('Dataset 4 shape: {}'.format(df4.shape))


df = df1
df = df1.append(df2)
df = df.append(df3)
df = df.append(df4)

df.index = np.arange(0,len(df))



p = df.groupby('Rating')['Rating'].agg(['count'])

# get movie count
movie_count = df.isnull().sum()[1]

# get customer count
cust_count = df['Cust_Id'].nunique() - movie_count

# get rating count
rating_count = df['Cust_Id'].count() - movie_count

ax = p.plot(kind = 'barh', legend = False, figsize = (15,10))
plt.title('Total pool: {:,} Movies, {:,} customers, {:,} ratings given'.format(movie_count, cust_count, rating_count), fontsize=20)
plt.axis('off')

for i in range(1,6):
    ax.text(p.iloc[i-1][0]/4, i-1, 'Rating {}: {:.0f}%'.format(i, p.iloc[i-1][0]*100 / p.sum()[0]), color = 'white', weight = 'bold')

"""
### Use below code to process each part one by one, also keep updating the movie_id variable

df_nan = pd.DataFrame(pd.isnull(df.Rating))
df_nan = df_nan[df_nan['Rating']==True]
print(df_nan.shape)

# create a single array with movie id - size ( difference of index) and value ( 1,2,3 etc)

movie_np = []

## We keep changing this variable by manually looking up the movie_id in one of those 4 data files
## As of now, this is to process the 4th part

#1,4500,9211,13368
movie_id = 13368

for i,j in zip(df_nan.index[1:],df_nan.index[:-1]):
#     print(i,j)
    temp_arr = np.full((1,i-j-1), movie_id)
    movie_np = np.append(movie_np,temp_arr)
    movie_id += 1

# last movie id

print(df_nan.iloc[-1, 0])

r = np.full((1,len(df1) - df_nan.index[-1] -1), movie_id)
#print(temp_arr)
movie_np = np.append(movie_np,r)
print(len(movie_np))

### Append the movie_np array as a column to the dataframe
###
df1 = df1[pd.notnull(df1['Rating'])]
#Add the movie_id column
df1['movie_id'] = movie_np.astype(int)
df1['user_id'] = df1['user_id'].astype(int)
print(df1.columns)
print('-Dataset examples-')
print(df1.iloc[::5000000,:])


new_cols = df1.columns.tolist()
new_cols = new_cols[:1]+new_cols[-1:]+new_cols[1:2]
df1 = df1[new_cols]

print("persist the processed file ")
processs_part = 'processed_part_4.csv'
output_dir = Path('trusted')

output_dir.mkdir(parents=True, exist_ok=True)
path_processed_part = os.path.join(output_dir, processs_part)  

df1.to_csv(path_processed_part, encoding='utf-8', index=False)
print('Stop analisys {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) )

