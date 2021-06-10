#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('../vacunes_100rt.csv', index_col=0)

sample = df.sample(1000, random_state=43623)
sample.to_csv('vacunes_100rt_evaluation1.csv')

sample = df.sample(1000, random_state=45031)
sample.to_csv('vacunes_100rt_evaluation2.csv')
