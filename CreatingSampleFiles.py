# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:56:09 2021

@author: DELL
"""

import pandas as pd

#as the file contains huge data so create small chunks of data
df_reader=pd.read_json('Clothing_Shoes_and_Jewelry.json',chunksize=1000000,lines=True)

counter = 1
for chunk in df_reader:
    #consider few samples for all types of reviews
    new_df = pd.DataFrame(chunk[['overall','reviewText','summary']])
    new_df1 = new_df[new_df['overall'] == 5].sample(4000)
    new_df2 = new_df[new_df['overall'] == 4].sample(4000)
    new_df3 = new_df[new_df['overall'] == 3].sample(8000)
    new_df4 = new_df[new_df['overall'] == 2].sample(4000)
    new_df5 = new_df[new_df['overall'] == 1].sample(4000)
    new_df6 = pd.concat([new_df1,new_df2,new_df3,new_df4,new_df5], axis = 0, ignore_index = True)
    new_df6.to_csv(str(counter)+".csv", index = False)
    
  
    counter +=1
    
    

