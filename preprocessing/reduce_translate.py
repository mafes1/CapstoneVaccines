
import pandas as pd
import numpy as np
import os
from datetime import datetime
from google_trans_new import google_translator

translator = google_translator()

def convert_date(date):

    date_time = datetime.strftime(datetime.strptime(date,'%Y-%m-%d %H:%M:%S+00:00'), '%Y-%m-%d %H:%M:%S')

    return date_time

def get_percentage(df, total):

    return (len(df) / len(total)) * 100

def get_quantity(df, total, final_length):

    return (get_percentage(df, total) * final_length) / 100

# CAT2 DATASET

# Import month files and merge into one file
df_cat = [pd.read_csv(os.path.join('data', 'CAT2', file), index_col=0) for file in os.listdir('data/CAT2')]
# all_cat = pd.concat(df_cat)
# all_cat.to_csv('data/CAT2/all_cat.csv')

# Import all CAT2 file and reduce
N = 25000
all_cat = pd.read_csv('data/all_cat.csv')

all_cat_red = []
for df_ in df_cat:
    df_['datetime'] = df_.date.apply(lambda x: convert_date(x))
    df_['datetime'] = pd.to_datetime(df_['datetime'], errors='coerce')
    red = df_.groupby(df_.datetime.dt.day, group_keys=False).apply(lambda x: x.sample(int(np.rint(get_quantity(df_, all_cat, N)*len(x)/len(df_))))).sample(frac=1).reset_index(drop=True)
    all_cat_red.append(red)

all_cat_red = pd.concat(all_cat_red)


all_cat['datetime'] = pd.to_datetime(all_cat['date'], errors='coerce')

all_cat.drop_duplicates(subset=['content'], inplace=True)
all_cat_red.drop_duplicates(subset=['content'], inplace=True)

# Export all_cat_red to csv file
# all_cat_red.to_csv('data/all_cat_reduced.csv')

all_cat['datetime'].hist(bins=280, xlabelsize=6)
all_cat_red['datetime'].hist(bins=280, xlabelsize=6)


# Divide and translate CAT>EN

# aug_sept = all_cat_red.loc[all_cat_red['datetime'] < datetime(2020, 10, 1), :].copy()
# aug_sept.loc[:, 'content'] = aug_sept.content.apply(lambda x: translator.translate(x, lang_tgt='en'))
# aug_sept.to_csv('data/EN2/aug_sept.csv')
#
# oct_nov = all_cat_red.loc[((all_cat_red['datetime'] > datetime(2020, 10, 1)) & (all_cat_red['datetime'] < datetime(2020, 12, 1))), :].copy()
# oct_nov.loc[:, 'content'] = oct_nov.content.apply(lambda x: translator.translate(x, lang_tgt='en'))
# oct_nov.to_csv('data/EN2/oct_nov.csv')

# dec = all_cat_red.loc[((all_cat_red['datetime'] > datetime(2020, 12, 1)) & (all_cat_red['datetime'] < datetime(2021, 1, 1))), :].copy()
# dec.loc[:, 'content'] = dec.content.apply(lambda x: translator.translate(x, lang_tgt='en'))
# dec.to_csv('data/EN2/dec.csv')

# gen = all_cat_red.loc[((all_cat_red['datetime'] > datetime(2021, 1, 1)) & (all_cat_red['datetime'] < datetime(2021, 2, 1))), :].copy()
# gen.loc[:, 'content'] = gen.content.apply(lambda x: translator.translate(x, lang_tgt='en'))
# gen.to_csv('data/EN2/gen.csv')

# feb = all_cat_red.loc[((all_cat_red['datetime'] > datetime(2021, 2, 1)) & (all_cat_red['datetime'] < datetime(2021, 3, 1))), :].copy()
# feb.loc[:, 'content'] = feb.content.apply(lambda x: translator.translate(x, lang_tgt='en'))
# feb.to_csv('data/EN2/feb.csv')

# mar = all_cat_red.loc[((all_cat_red['datetime'] > datetime(2021, 3, 1)) & (all_cat_red['datetime'] < datetime(2021, 4, 1))), :].copy()
# mar.loc[:, 'content'] = mar.content.apply(lambda x: translator.translate(x, lang_tgt='en'))
# mar.to_csv('data/EN2/mar.csv')

# ab = all_cat_red.loc[((all_cat_red['datetime'] > datetime(2021, 4, 1)) & (all_cat_red['datetime'] < datetime(2021, 5, 1))), :].copy()
# ab.loc[:, 'content'] = ab.content.apply(lambda x: translator.translate(x, lang_tgt='en'))
# ab.to_csv('data/EN2/ab.csv')

# Create CAT>EN file
# df_en = [pd.read_csv(os.path.join('data', 'EN2', file), index_col=0) for file in os.listdir('data/EN2')]
# df_reduced_en = pd.concat(df_en)
# df_reduced_en.to_csv('data/cat_vaccines_en.csv')