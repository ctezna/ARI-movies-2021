#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 19:28:22 2021

@author: usuario
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from datetime import datetime

from collections import OrderedDict
probe_file = open("archive/probe.txt","r")
lines = probe_file.read().split("\n")

movie_id_dict = {}
prev_index = 0
prev_value = 1

valueList = []

for i in range(len(lines)):
    if(":" in lines[i]):
        movie_id_dict[str(prev_value)] = i-prev_index-1
        prev_index = i
        prev_value = int(lines[i].split(":")[0])
    else:
        valueList.append(lines[i])
    
movie_id_dict[str(prev_value)] = len(lines)-prev_index-1

orderedDict = OrderedDict(sorted(movie_id_dict.items()))

movie_np = []
## Create np array based on the ordered dict 

for k,v in orderedDict.items():
    temp_arr = np.full((1,v), int(k))
    movie_np = np.append(movie_np,temp_arr)

        
df = pd.DataFrame(valueList,columns=['user_id'])
df['movie_id'] = movie_np.astype(int)

print("persist the processed file ")
processs_part = 'processed_probe.csv'
output_dir = Path('trusted')

output_dir.mkdir(parents=True, exist_ok=True)
path_processed_part = os.path.join(output_dir, processs_part)  

df.to_csv(path_processed_part, encoding='utf-8', index=False)
print('Stop analisys {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) )