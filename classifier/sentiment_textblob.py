#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 23:09:38 2021

@author: marti
"""
#%% Libraries and data
import pandas as pd
from textblob import TextBlob

df = pd.read_csv('data/EN/vacunes_100rt_en.csv', index_col=0)
df = df[df.columns[1:]]

#%% Sentiment
def get_polarity(text):
    return TextBlob(text).sentiment

sentiment = df['content'].apply(get_polarity)

df['polarity'] = sentiment.apply(lambda x: x[0])
df['subjectivity'] = sentiment.apply(lambda x: x[1])

#%%
df.to_csv('data/EN/vacunes_100rt_en_textblob_vader.csv')
