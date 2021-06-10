# %% Libraries
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from google_trans_new import google_translator
from time import time

# %% Scraping per word
#import locale
#locale.setlocale(locale.LC_ALL, 'en_GB')
# df_vaccines = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
#     'vacuna since:2020-8-01 until:2020-9-01 lang:ca').get_items(), 99999))[['date', 'content', 'id', 'user', 'replyCount', 'retweetCount', 'likeCount', 'lang']]
#
# df_vaccines.to_csv('vacunes_august2.csv')

df_vaccines = pd.read_csv('data/CAT/vacunes_april2.csv')


df_vaccines['datetime'] = pd.to_datetime(df_vaccines['date'], errors='coerce')


df_vaccines['datetime'].hist(bins=30, xlabelsize=6)



# translator = google_translator()

# df_vaccines.content = df_vaccines.content[:2500].apply(lambda x: translator.translate(x, lang_tgt='en'))
# df_vaccines.to_csv('vacunes_en.csv')


# Calculate sampling size
# Stratified random sampling

# Pick random stratified subsample
N = 5000
df_reduced = df_vaccines.groupby(df_vaccines.datetime.dt.day, group_keys=False).apply(lambda x: x.sample(int(np.rint(N*len(x)/len(df_vaccines))))).sample(frac=1).reset_index(drop=True)

# %% Scraping per RT
#df_reduced['datetime'].hist(bins=30, xlabelsize=6)
from time import time

init = time()
df_vaccines = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
    '(vacuna) since:2020-8-01 until:2021-5-01 min_retweets:100').get_items(), 100000))
final = time()
print(final-init)
df_vaccines.date.hist(bins=30)
df_vaccines['username'] = df_vaccines['user'].apply(lambda x: x['username'])

print(df_vaccines.date.max() - df_vaccines.date.min() )