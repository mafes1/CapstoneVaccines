import pandas as pd
from google_trans_new import google_translator
import re

sample2 = pd.read_csv('data/df_sample_en2.csv')

# Recuperar contingut i traduir-lo
translator = google_translator()
tweet = sample2.renderedContent[455]
tweet = re.sub('\?{3}', '', tweet)
translated = translator.translate(tweet, lang_tgt='en')

# Substituir contingut actual pel tuit traduït
sample2.content.replace(to_replace='??? ', value=translated, inplace=True)

# Corregir labels
sample2.label.replace(to_replace='por', value='pos', inplace=True)
sample2.label.fillna('pos', inplace=True)

sample2.to_csv(('data/df_sample_en2-455.csv'))
