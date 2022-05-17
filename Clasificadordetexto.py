from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer


#from nltk import SnowballStemmer
#spanishstemmer=SnowballStemmer("spanish")

from string import punctuation



#Cargamos el data set de las noticias
dfnoticias=pd.read_csv("datasetnoticias2.csv", encoding= 'unicode_escape', delimiter=";")
#Cargamos las noticias y la categoria
Noticias=dfnoticias["Titular"].values.astype('U')


#Cargamos las stop words en español
swsp = pd.read_fwf('Stop Words Spanish.txt', header=None)
stopwordsspanish=swsp[0].to_numpy()
#Creamos el count vectorizer con las stopwords en español
cv=CountVectorizer(stop_words=list(stopwordsspanish), preprocessor=lambda x: re.sub(r'(\d[\d\.])+', 'NUM', x.lower()))
#print(cv)
listasw=list(stopwordsspanish)
#Convertimos las categorias en numeros, existen 13 categorias
Categorias=dfnoticias["Categoria"]
encoder=LabelEncoder()
dfnoticias['Categorianum']=encoder.fit_transform(dfnoticias.Categoria.values)
#print(dfnoticias['Categorianum'])

#Usamos la clase count vectorizer para transformar las noticias en vectores
noticiasvector=cv.fit_transform(Noticias)

#print("--------")
#print(cv.vocabulary_.get(u'algorithm'))
#De ocurrencias a frecuencias, 
tfidf_transformer = TfidfTransformer()
Noticiastfidf = tfidf_transformer.fit_transform(noticiasvector)
#print(Noticiastfidf.shape)
#Creando clasificador Naive Bayes Multinomial
clf = MultinomialNB().fit(Noticiastfidf, dfnoticias['Categorianum'])

#Poniendo a prueba el entrenamiento
"""
noticiasnuevas=["Niños tributarán por bajar un libro por IVA a servicios digitales", "Bolívar tiene el arco en cero frente a Wilstermann"]
X_new_counts = cv.transform(noticiasnuevas)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
predicted = clf.predict(X_new_tfidf)

print(predicted)
print(encoder.inverse_transform(predicted))
"""
from numpy import dot
from numpy.linalg import norm
cos_sim = lambda a, b: dot(a, b)/(norm(a)*norm(b))
def sacarcategoria(titulardelanoticia):
    arrayaux=[]
    arrayaux.append(titulardelanoticia)
    matrixnot=cv.transform(arrayaux)
    tfidaux=tfidf_transformer.transform(matrixnot)
    predicted = clf.predict(tfidaux)
    categoria=encoder.inverse_transform(predicted)[0]
    return categoria


def descubrircategoriaporenlace(enlace):
    enlace=enlace.replace("/"," ")
    enlace=enlace.replace("-"," ")
    retornar=""
    estaclaro=False
    categorias=["politica", "economia", "seguridad", "deportes",  "universidad", "entretenimiento", "ciencia","tecnologia", "cultura", "salud","medioambiente", "internacional"]
    categoriasdud=["sociedad","nacional", "Bolivia"]
    for categoria in categorias:
        if categoria.upper() in enlace.upper():
            retornar=categoria.upper()
            if categoria=="ciencia" or categoria=="tecnologia":
                retornar="CIENCIA Y TEGNOLOGIA"
            if categoria=="planeta" or categoria=="mundo":
                retornar="INTERNACIONAL"
            estaclaro=True
    for categoria in categoriasdud:
        if categoria.upper() in enlace.upper():
            retornar=categoria.upper()
            if categoria=="Bolivia":
                retornar="NACIONAL"
    return retornar, estaclaro
"""
def normalize(text):
    doc = nlp(text)
    words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
    lexical_tokens = [t.lower() for t in words if len(t) > 3 and     
    t.isalpha()]
    return lexical_tokens
def lematizartexto(text):
    doc = nlp(text)
    lemmas = [tok.lemma_.lower() for tok in doc]
    textoproc=' '.join(lemmas)
    return textoproc
def radicalizartexto(text):
    tokens = normalize(text) # crear una lista de tokens
    stems = [spanishstemmer.stem(token) for token in tokens]
    textoproc=' '.join(stems)
    return textoproc


def similaridadcoseno(texto1, texto2):
    texto1=lematizartexto(texto1)
    texto2=radicalizartexto(texto2)
    texto1=radicalizartexto(texto1)
    texto2=radicalizartexto(texto2)
    #print(texto1)
    #print(texto2)
    arrayaux=[]
    arrayaux.append(texto1)
    arrayaux.append(texto2)
    matrixtext=cv.transform(arrayaux)
    tfidaux=tfidf_transformer.transform(matrixtext)
    #print("vector1: ",tfidaux.toarray()[0])
    #print("vector2: ",tfidaux.toarray()[1])
    return cos_dist(tfidaux.toarray()[0], tfidaux.toarray()[1])*100
#print(sacarcategoria(""))
#cat,bol=descubrircategoriaporenlace("https://jornada.com.bo/seccion/salud/")

#print("categoria: ", cat, bol)

"""  
def cos_dist(vec1,vec2):
    """
         : param vec1: vector 1
         : param vec2: vector 2
         : return: devuelve la similitud coseno de dos vectores
    """
    a=float(np.dot(vec1,vec2))
    b=float(np.linalg.norm(vec1)*np.linalg.norm(vec2))

    if b==0:
        a=0
        b=1
    dist1=a/b
    return dist1

#print(similaridadcoseno("Francia reelige al centrista Macron ante una extrema derecha en progresión", "Balotaje: Macron gana las presidenciales y desplaza por segunda vez a la ultraderecha"))
"""
def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result # 5
"""
def eliminarstopwords(texto):
    return ' '.join([word for word in texto.split(' ') if word not in listasw])
#print(eliminarstopwords("Policía aprehende a un menor de edad por un caso de feminicidio"))

#print(get_hotwords("Luego de 10 años, la festividad del Gran Poder terminó su contrato con una conocida cervecera nacional como principal auspiciadora. Así lo confirmó la Asociación de Conjuntos Folklóricos del Gran Poder (ACFGP), que informó que el nuevo patrocinador será una cervecera de origen brasilero."))