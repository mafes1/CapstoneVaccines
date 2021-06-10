# %% 
import pandas as pd, os, numpy as np, csv, re, nltk, string, snowballstemmer
from collections import Counter

dfs = [ pd.read_csv(os.path.join('..', 'data', 'CAT', file), index_col=0) for file in os.listdir('..', 'data/CAT') ]
df = pd.concat(dfs)

original_size = np.array([df.shape[0] for df in dfs])

df.reset_index(drop=True, inplace=True)

# %%

df.drop_duplicates(subset=['date', 'content'], keep='last', inplace=True) # remove date?

# %% Extracción de los emoticionos y su frecuencia

def extract_emojis(text):
    emojis = []
    for char in text:
        if ord(char) > 600: emojis.append(char)
    return emojis

emojis_lists = df.content.apply(extract_emojis).tolist()

emojis = Counter( [emoji for emojis_list in emojis_lists for emoji in emojis_list] )

with open('emojis.csv', "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(emojis.most_common())

# %% Replace emojis for definition. El fichero emojis.csv se ha copiado como emojis_dict.csv y una columna se ha añadido a mano, rellenando solo los más populares y fáciles

with open('emojis_dict.csv') as csvfile:
    emojis = {}
    emojis_ranking = []
    reader = csv.reader(csvfile)
    for i in reader:
        if len(i) > 2:
            emojis[i[0]] = i[-1]
            emojis_ranking.append(i)
            
# %% Vocabulario informal a partir de carácteres que no sean emoticonos

slang_data = {}
slang_data[':)'] = r'contento'
slang_data[':-)'] = r'contento'
slang_data[':D'] = r'contento'
slang_data[':-D'] = r'contento'

slang_data[':*'] = r'beso'

slang_data[":'("] = r'triste'
slang_data[':('] = r'triste'
slang_data[':-('] = r'triste'
slang_data['TT'] = r'triste'

# %% Se separan hashtags y se añaden al final del tuit. ¿Borrarlos?

def clean_full_text(text):
    hashtags = []
    #expanded = " ".join([re.sub(r'[#\s]', '', a) for a in re.split('([A-Ź]*[a-ź]+)', row['full_text']) if a and not re.match(r'^\s$', a)])
    hashtags_ = re.findall(r'#[A-ZÀ-ßa-zà-ý]+', text)
    for hashtag in hashtags_:
        text = re.sub(hashtag, '', text)
        expanded = " ".join([re.sub(r'[#\s]', '', token) for token in re.split(r'([A-ZÀ-ß][a-zà-ý]*)', hashtag) if token and not re.match(r'^\s$', hashtag)]).strip()
        expanded = re.sub(r'\b(\S)\s+(?=\S\b)', r'\1', expanded)
        hashtags.append(expanded)

    text = re.sub(r'\s', ' ', text + '. '.join(hashtags))
    
    return text

# %% Aplicar funciones

df['preprocessed_text'] = df.content.apply(clean_full_text)
for key, value in emojis.items(): df['preprocessed_text'] = df['preprocessed_text'].str.replace(key,' ' +  value + ' ')# 'emoji ')


df['preprocessed_text'] = df['preprocessed_text'].str.lower()
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat=r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', repl=' ', regex=True)
df['slang_data'] = 0
for key, value in slang_data.items():
    df['slang_data'] += df['preprocessed_text'].str.count(pat=re.escape(key))
    df['preprocessed_text'] = df.preprocessed_text.str.replace(pat=re.escape(key), repl=' ' + value + ' ', regex=True)
    

# %% Características, limpieza general y tokenización

stemmer = nltk.snowball.SnowballStemmer("spanish") #se se descomenta, comentar el stemmer para catalán y la limpieza para catalán, y descomentar la limpieza para castellano

#stemmer = snowballstemmer.stemmer('catalan') #el algoritmo para catalán no está en la biblioteca nltk

#df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat=r"\b" + r'\b|\b'.join(stopwords) + r"\b", repl=' ', regex=True)
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat=r"\d", repl=' ', regex=True) #remove numbers
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat='[' + re.escape('?¿') + ']', repl=' pregunta ', regex=True)
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat='[' + re.escape('!¡') + ']', repl=' exclamacion ', regex=True)
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat='[' + re.escape('?¿') + ']', repl=' ', regex=True)
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat='[' + re.escape('!¡') + ']', repl=' ', regex=True)
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat='[' + re.escape(string.punctuation) + r'\n\t]', repl=' ', regex=True)
df['preprocessed_text'] = df['preprocessed_text'].str.strip()
df['preprocessed_text'] = df['preprocessed_text'].str.replace(pat=r'\s+', repl=' ', regex=True)
#df['preprocessed_text'] = df['preprocessed_text'].str.split().apply( lambda x: ' '.join(stemmer.stemWords (x)))# para catalán
df['preprocessed_text'] = df['preprocessed_text'].apply(stemmer.stem )# para castellano

df['punctuation'] = df['content'].str.count(pat='[' + re.escape(string.punctuation) + r'!¿?¡]')

# %%

df.to_csv('tweets_preprocessed.csv')
