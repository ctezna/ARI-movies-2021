#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 20:32:15 2021

@author: usuario


import shutil
csv_files = ['source1.csv', 'source2.csv', 'source3.csv', 'source4.csv', 'source5.csv']
target_file_name = 'dest.csv';
shutil.copy(csv_files[0], target_file_name)
with open(target_file_name, 'a') as out_file:
    for source_file in csv_files[1:]:
        with open(source_file, 'r') as in_file:
#             if your csv doesn't contains header, then remove the following line.
            in_file.readline()
            shutil.copyfileobj(in_file, out_file)
            in_file.close()
    out_file.close()
"""

import pandas as pd
df_train_1 = pd.read_csv('trusted/processed_part_1.csv')
df_train_2 = pd.read_csv('trusted/processed_part_2.csv')
df_train_3 = pd.read_csv('trusted/processed_part_3.csv')
df_train_4 = pd.read_csv('trusted/processed_part_4.csv')
print('laod dataframe')
df_train = pd.concat([df_train_1, df_train_2,df_train_3,df_train_4], ignore_index=True)
print(df_train.head(10))

import numpy as np
df_probe = pd.read_csv('trusted/processed_probe.csv')
df_probe['Rating'] = np.nan
print(df_probe.head(10))

print("length of train df")
print(len(df_train))

print()

print("length of probe df")
print(len(df_probe))

df_probe['movie_id'] = df_probe['movie_id'].astype(int)

keys = ['user_id', 'movie_id']
i1 = df_train.set_index(keys).index
i2 = df_probe.set_index(keys).index
df_pure_train =  df_train[~i1.isin(i2)]
df_pure_train.to_csv('trusted/all_4_train.csv', encoding='utf-8', index=False)
print('Saved all_4_train.csv')

## Now get probe
i3 = df_pure_train.set_index(keys).index
df_pure_probe = df_train[~i1.isin(i3)]


df_pure_probe.to_csv('trusted/all_4_probe.csv', encoding='utf-8', index=False)
print('Saved all_4_probe.csv')