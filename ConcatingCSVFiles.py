# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 20:17:29 2021

@author: DELL
"""
import pandas as pd
from glob import glob
from datetime import datetime


startime=datetime.now()
filenames=glob('*.csv')

dataframes=[pd.read_csv(f) for f in filenames]

frame=pd.concat(dataframes,axis=0,ignore_index=True)

frame.to_csv('balanced_review.csv',index=False)





print(datetime.now() - startime)