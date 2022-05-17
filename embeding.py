from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import pandas as pd
import numpy as np
import re
dfnoticias=pd.read_csv("noticias.csv", encoding= 'unicode_escape', delimiter=";")

"""data=['I love play Tennis', "Mia hate play Tennis", "Caroline played Tennis all Night"]
cv=CountVectorizer(stop_words='english')
data=cv.fit_transform(data)

print(cv.vocabulary_)




palabras=dict(zip(cv.get_feature_names(),tfidtransformer.idf_))

for palabra, puntuacion in palabras.items():
    print(palabra, puntuacion)

print("Evo: ",palabras["evo"])
"""
def no_number_preprocessor(tokens):
    r = re.sub('(\d)+', 'NUM', tokens.lower())
    # This alternative just removes numbers:
    # r = re.sub('(\d)+', '', tokens.lower())
    return r
Noticias=dfnoticias["Titular"].values.astype('U')
Categorias=dfnoticias["Categoria"]
swsp = pd.read_fwf('Stop Words Spanish.txt', header=None)
stopwordsspanish=swsp[0].to_numpy()

print(Noticias)
print("--------------")
print(stopwordsspanish)
print("-----------------")
for i in range(0,200):
    print(Noticias[i])
cv=CountVectorizer(stop_words=list(stopwordsspanish), preprocessor=lambda x: re.sub(r'(\d[\d\.])+', 'NUM', x.lower()))


vectorizer=TfidfVectorizer()

X_tfid=vectorizer.fit_transform(Noticias)
print(X_tfid)

from sklearn.metrics.pairwise import cosine_similarity
sims=cosine_similarity(X_tfid[0:2], X_tfid)

texto=""
print(sims)