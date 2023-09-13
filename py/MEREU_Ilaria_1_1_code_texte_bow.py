# -*- coding: utf-8 -*-
"""MEREU_Ilaria_1_1_texte_bow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DHnNXdfmjcWLhlpu2eV6VUue3f_To6UH

Ce fichier est le premier sur quatre. Nous allons ici traiter les textes avec les approches BoW (Bag of Words).
"""

#Initialisation
import pandas as pd

import sys
!{sys.executable} -m pip install nltk
import nltk

!{sys.executable} -m pip install sklearn

# !{sys.executable} -m pip install gensim
# !{sys.executable} -m pip install pyLDAvis
# !{sys.executable} -m pip install tensorflow


# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# import gensim

from sklearn.feature_extraction.text import TfidfVectorizer

from collections import defaultdict
import matplotlib.pyplot as plt

import numpy as np

nom_source = "data/source/Flipkart/flipkart_com-ecommerce_sample_1050.csv"
df = pd.read_csv(nom_source, sep= ',', low_memory=False )

display(df.shape)
df.info()

"""# 1.1.1 Traitement des textes


1.   Tokenisation
2.   Stopwords
3. Lemmatisation
4. Création fonction de combinaison de la description avec le nom du produit
5. Choix du texte pour le corpus (description, nom du produit, ou combinaison des deux) pour la création des bags of words
"""

# Tokenizer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

import re

def tokenizer_fct(sentence) :
    # print(sentence)
    sentence_clean = sentence.replace('-', ' ').replace('+', ' ').replace('/', ' ').replace('#', ' ')
    word_tokens = word_tokenize(sentence_clean)
    return word_tokens

# Stop words
from nltk.corpus import stopwords
stop_w = list(set(stopwords.words('english'))) + ['[', ']', ',', '.', ':', '?', '(', ')', '-']

stopwords_specific = ['pack', 'set', 'combo', 'box',
                      'jaipur', 'elegance', 'shape',  'print',  'light', 'led',
                      'rockmantra', 'eurospa', 'terry',
                     'printed','usb', 'print',
                     'double', 'single',
                     'red', 'brown', 'black', 'multicolor', 'blue', 'color', 'green',
                      'abstract', 'floral',
                     'vinyl', 'ideal',
                     'large', 'comfort', 'extra', 'sized', 'height', 'width', 'lenght',
                     'polyester', 'crystal', 'ceramic', 'paper', 'cotton', 'porcelain',
                     'lapguard', 'sstudio', 'sonata', 'vgn', 'vaio',
                     'gathered', 'printland', 'prithish', 'hot', 'product','maximum']

stop_w = stop_w + stopwords_specific

def stop_word_filter_fct(list_words) :
    filtered_w = [w for w in list_words if not w in stop_w]
    filtered_w2 = [w for w in filtered_w if len(w) > 2]
    return filtered_w2

# lower case et alpha
def lower_start_fct(list_words) :
    lw = [w.lower() for w in list_words if (not w.startswith("@"))]
    #                                   and (not w.startswith("#"))
    #                                    and (not w.startswith("http"))]
    return lw

# Lemmatizer (base d'un mot)
from nltk.stem import WordNetLemmatizer

def lemma_fct(list_words) :
    lemmatizer = WordNetLemmatizer()
    lem_w = [lemmatizer.lemmatize(w) for w in list_words]
    return lem_w

# Fonction de préparation du texte pour le bag of words (Countvectorizer et Tf_idf, Word2Vec)
def transform_bow_fct(desc_text) :
    word_tokens = tokenizer_fct(desc_text)
    sw = stop_word_filter_fct(word_tokens)
    lw = lower_start_fct(sw)
    # lem_w = lemma_fct(lw)
    transf_desc_text = ' '.join(lw)
    return transf_desc_text

# Fonction de préparation du texte pour le bag of words avec lemmatization
def transform_bow_lem_fct(desc_text) :
    word_tokens = tokenizer_fct(desc_text)
    sw = stop_word_filter_fct(word_tokens)
    lw = lower_start_fct(sw)
    lem_w = lemma_fct(lw)
    transf_desc_text = ' '.join(lem_w)
    return transf_desc_text

# Fonction de préparation du texte pour le Deep learning (USE et BERT)
def transform_dl_fct(desc_text) :
    word_tokens = tokenizer_fct(desc_text)
#    sw = stop_word_filter_fct(word_tokens)
    lw = lower_start_fct(word_tokens)
    # lem_w = lemma_fct(lw)
    transf_desc_text = ' '.join(lw)
    return transf_desc_text

# Création d'un texte extrait de la description par l'intersection avec le nom du produit
def transform_descr_new() :
    s_i = []

    for i in range(len((df['description'].values))):
    # j = str().split(" ")
    # n = str(df['product_name'].values[i]).replace('-', '').split(" ")

        j = tokenizer_fct(df['description'].values[i])
        j = lower_start_fct(j)
        n = tokenizer_fct(df['product_name'].values[i])
        n = lower_start_fct(n)

        for w in n :
            # print(w, len(w))
            if not w.isalpha() or len(w)<3:
                n.remove(w)

        if '' in n:
            n.remove('')

        # print(n)
        s = ''
        for w in j:
            # print(w)
            if w in n and w not in stopwords_specific:
                # print(w, 'ok')
                s = s + ' ' + w

        s_i.append(s)

    df['descr_new'] = pd.Series(s_i)

transform_descr_new()

df.head()

feats = ['description', 'product_name', 'descr_new']

feat_start = feats[2]

df['sentence_bow'] = df[feat_start].apply(lambda x : transform_bow_fct(x))
df['sentence_bow_lem'] = df[feat_start].apply(lambda x : transform_bow_lem_fct(x))
df['sentence_dl'] = df[feat_start].apply(lambda x : transform_dl_fct(x))
df['len_d'] = df['sentence_bow'].apply(len)+df['sentence_bow_lem'].apply(len)+(df['sentence_dl']).apply(len)

df.head()

"""# 1.1.2 Élaboration des catégories"""

# df['first_category'] = df['product_category_tree'].str.extract(r'\[\"(\w* \w*)')
df['first_category'] = df['product_category_tree'].str.extract(r'^\[\"(.+?)[\>\>]')
df['second_category'] = df['product_category_tree'].str.extract(r'[\>\>](.+?)[\>\>]').replace(r'\> ', '', regex=True)
df['third_category'] = df['product_category_tree'].str.extract(r'[\>\>].+?[\>\>](.+?)[\>\>]').replace(r'\> ', '', regex=True)
df['fourth_category'] = df['product_category_tree'].str.extract(r'[\>\>].+?[\>\>].+?[\>\>](.+?)[\>\>]').replace(r'\> ', '', regex=True)
df['fifth_category'] = df['product_category_tree'].str.extract(r'[\>\>].+?[\>\>].+?[\>\>].+?[\>\>](.+?)').replace(r'\> ', '', regex=True)

df.head()

# Definizione l_cat e studio delle categorie
cat_N1 = df.groupby(by='first_category').count().index.to_list()
display(df.groupby(by='first_category').count())

cat_N2 = df.groupby(by='second_category').count().index.to_list()
# display(len(df.groupby(by='second_category').count().index.to_list()))

l_cat = cat_N1

print("catégories : ", l_cat)
# y_cat_num = [(1-l_cat.index(df.iloc[i]['first_category'])) for i in range(len(df))]
y_cat_num = [(l_cat.index(df.iloc[i]['first_category'])) for i in range(len(df))]
print(y_cat_num)

"""# 1.2 Texte - Bag of Words
Création des bags of words, réduction de dimensionalité, clustering pour un k fixé

***Créations des bags of words***
"""

# %%script false --no-raise-error
from sklearn import cluster, metrics

# création du bag of words (CountVectorizer et Tf-idf)

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import manifold

cvect = CountVectorizer(stop_words='english', max_df=0.95, min_df=1) # approche 1 - CV
ctf = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=1) # approche 2 - td-idf

feat = 'sentence_bow_lem'
cv_fit = cvect.fit(df[feat]) # approche 1 - CV
ctf_fit = ctf.fit(df[feat]) # approche 2 - td-idf

cv_transform = cvect.transform(df[feat]) # approche 1 - CV
ctf_transform = ctf.transform(df[feat]) # approche 2 - td-idf

"""***Réduction de dimensions (PCA et t-SNE) et clustering avec k fixé***"""

# Commented out IPython magic to ensure Python compatibility.
# %%script false --no-raise-error
# #Cellule résultats
# from sklearn.decomposition import PCA
# import time
# 
# #PCA reduction
# def pca_fct(df, graph=True):
#     pca = PCA(n_components=0.9, random_state=42, svd_solver ='full').fit(df) # svd_solver = 'full'
#     # If 0 < n_components < 1 and svd_solver == 'full', select the number of components
#     # such that the amount of variance that needs to be explained is greater
#     # than the percentage specified by n_components.
#     X = pca.transform(df)
# 
#     return X
# 
# # Modified for t-SNE calculation and visualisation
# def tSNE_e_kmeans(features, y_cat_num, num_clusters) :
#     time1 = time.time()
#     num_labels=len(l_cat)
#     tsne = manifold.TSNE(n_components=2, perplexity=30, n_iter=2000,
#                                  init='random', learning_rate=200, random_state=42)
#     X_tsne = tsne.fit_transform(features)
# 
#     # Détermination des clusters à partir des données après Tsne
#     cls = cluster.KMeans(n_clusters=num_clusters, n_init=100, random_state=42)
#     cls.fit(X_tsne)
# 
#     time2 = np.round(time.time() - time1,0)
#     print("tsne + clustering time : ", time2)
# 
#     labels = cls.labels_
# 
#     fig = plt.figure(figsize=(15,6))
# 
#     ax = fig.add_subplot(121)
#     scatter = ax.scatter(X_tsne[:,0],X_tsne[:,1], c=y_cat_num, cmap='Set1')
#     ax.legend(handles=scatter.legend_elements()[0], labels=l_cat, loc="best", title="Catégorie")
#     plt.title('Représentation des produits par catégories réelles')
# 
#     ax = fig.add_subplot(122)
#     scatter = ax.scatter(X_tsne[:,0],X_tsne[:,1], c=labels, cmap='Set1')
#     ax.legend(handles=scatter.legend_elements()[0], labels=set(labels), loc="best", title="Clusters")
#     plt.title('Représentation des produits par clusters')
# 
#     plt.show()
# 
#     ARI = np.round(metrics.adjusted_rand_score(y_cat_num, labels),4)
#     time2 = np.round(time.time() - time1,0)
#     print("n_clusters: %s\n" % num_clusters, "ARI : ", ARI, "time : %s \n\n-----------------------" % time2)
# 
# def bag_of_words(vect_for_pca, ind_vectorizer):
#     # ind_vectorizer - 0 for count vectoriser
#     # ind_vectorizer - 1 for Tfid
#     vectorizer = vectorizers[ind_vectorizer][0]
#     print('Vectorisation method: %s' % vectorizers[ind_vectorizer][1])
#     # fit et trasformation d'une colonne du dataframe, on obtient une sparse matrix
#     cvect_ft = vectorizer.fit_transform(vect_for_pca.astype('U')) 
#     # PCA refuserait ce format, donc -> 
#     
#     # print(cvect_ft)
#     # print(cvect_ft.dtype, cvect_ft.shape)
#     feature_names = vectorizer.get_feature_names()
# 
#     df_for_pca = pd.DataFrame(cvect_ft.toarray(),columns=feature_names) 
#     # -> d'une sparse matrix à dataframe accepté par PCA
# 
#     X = pca_fct(df_for_pca) # Vectorisation du corpus
# 
#     tSNE_e_kmeans(X, y_cat_num, num_labels)
#     # tSNE_e_kmeans(X, y_cat_num, 5) # le nombre de clusters peut être librement fixé ici
# 
# scegli_vect_for_pca = [df['sentence_bow_lem']]
# nomi_scegli_vect_for_pca = ['df[\'sentence_bow_lem\']']
# num_labels=len(l_cat)
# n = 0
# for i_data in range(len(scegli_vect_for_pca)):
#     vect_for_pca = scegli_vect_for_pca[i_data]
#     print(i_data, nomi_scegli_vect_for_pca[i_data])
# 
#     for j_ind_vectorizer in (0, 1):
#         n += 1
#         print(n)
#         cvect = CountVectorizer(encoding='utf-8', strip_accents='unicode', stop_words=stop_w, max_df=0.95, min_df=1) # approche 1 - CV
#         ctf = TfidfVectorizer(encoding='utf-8', strip_accents='unicode', stop_words=stop_w, max_df=0.95, min_df=1) # approche 2 - td-idf
#         vectorizers = [[cvect, 'CountVectorizer'], [ctf, 'TfidfVectorizer']]
#         vectorizer = vectorizers[j_ind_vectorizer][0]
# 
#         vect_for_pca = scegli_vect_for_pca[i_data]
#         bag_of_words(vect_for_pca, j_ind_vectorizer)
#         print("Bag of words")
#         print("Vectorizer: %s" % vectorizers[j_ind_vectorizer][1])
#         print("Texte: %s" % nomi_scegli_vect_for_pca[i_data])
#         print("n_clusters: %s\n\n-----------------------\n\n" % nomi_scegli_vect_for_pca[i_data])
# 
# #cvect_ft.get_feature_names_out()
# # print(X)

"""# 1.3 Approche k variable

Les fonctions reflètent l'approche de balayer un interval de valeurs pour k.
"""

# %%script false --no-raise-error
# Cellule résultats et tableau

from sklearn.decomposition import PCA
import time

# Écriture di stdout and stderr dans un fichier exterieur
# sys.stdout = open('out.log', 'w')
# sys.stderr = sys.stdout

def for_table(ind_feat, ind_vectorizer, num_clusters):
# ----------------- ok 7 ------ok 15 --------- ok 40 -----
    feat_start = feats[ind_feat]
    df['sentence_bow_lem'] = df[feat_start].apply(lambda x : transform_bow_lem_fct(x))

    cvect = CountVectorizer(encoding='utf-8', strip_accents='unicode', stop_words=stop_w, max_df=0.95, min_df=1) # approche 1 - CV
    ctf = TfidfVectorizer(encoding='utf-8', strip_accents='unicode', stop_words=stop_w, max_df=0.95, min_df=1) # approche 2 - td-idf
    vectorizers = [[cvect, 'CountVectorizer'], [ctf, 'TfidfVectorizer']]
    # ind_vectorizer - 0 for count vectoriser
    # ind_vectorizer - 1 for Tfid
    vectorizer = vectorizers[ind_vectorizer][0]

    vect_for_pca = df['sentence_bow_lem']

    # fit e trasforma una colonna del dataframe e ne ottiene una sparse matrix
    cvect_ft = vectorizer.fit_transform(vect_for_pca.astype('U')) #Se questa la passi a PCA direttamente la rifiuta perché è una sparse matrix. Vedi errore 4

    feature_names = vectorizer.get_feature_names()

    df_for_pca = pd.DataFrame(cvect_ft.toarray(),columns=feature_names) # da sparse matrix a dataframe accettato da PCA

    pca = PCA(n_components=0.9, random_state=42, svd_solver ='full').fit(df_for_pca) # svd_solver = 'full'
    # If 0 < n_components < 1 and svd_solver == 'full', select the number of components
    # such that the amount of variance that needs to be explained is greater
    # than the percentage specified by n_components.
    X = pca.transform(df_for_pca)

    # tSNE_e_kmeans
    time1 = time.time()
    num_labels=len(l_cat)
    tsne = manifold.TSNE(n_components=2, perplexity=30, n_iter=2000,
                                 init='random', learning_rate=200, random_state=42)
    X_tsne = tsne.fit_transform(X)

    # Détermination des clusters à partir des données après Tsne
    cls = cluster.KMeans(n_clusters=num_clusters, n_init=100, random_state=42)
    cls.fit(X_tsne)

    time2 = np.round(time.time() - time1,0)

    labels = cls.labels_

    ARI = np.round(metrics.adjusted_rand_score(y_cat_num, labels),4)
    time2 = np.round(time.time() - time1,0)

    return ARI


filenamef = "comparaison-bow.txt"
f = open(filenamef, 'w')

num_labels=len(l_cat)
n = 0
feats = ['description', 'product_name', 'descr_new']
vectorizers = [[cvect, 'CountVectorizer'], [ctf, 'TfidfVectorizer']]

for ind_feat in range(1, len(feats)):
    for ind_vectorizer in (0, 1):
        for num_clusters in range(4, 65):

            ARI = for_table(ind_feat, ind_vectorizer, num_clusters)

            print("%s - %s - %s - %s"  % ( feats[ind_feat], vectorizers[ind_vectorizer][1], num_clusters, ARI))
            f.write("%s - %s - %s - %s\n"  % ( feats[ind_feat], vectorizers[ind_vectorizer][1], num_clusters, ARI))

f.close

"""Graphique de comparaison de la performance selon le nombre de clusters


"""

# %%script false --no-raise-error

x = np.arange(4, 65)
x_df = pd.Series(x)

lab = ["CV - description", "td-idf - description", "CV - nom", "td-idf - nom", "CV - description + nom", "td-idf - description + nom"]
#for i in range(0, 6):
for i in (0, 2, 4, 1, 3, 5):
    # print(i)
    #source_bow = 'traitement-bow/bow-tr-%s.txt' % i
    source_bow = 'traitement-bow/bow-tr-%sb.txt' % int(i+1)
    df = pd.read_csv(source_bow, sep= ' ', low_memory=False )
    df.columns = ['clusters', 'ARI']
    plt.xlim(4, 30)

    plt.plot(df['clusters'], df['ARI'], label = lab[i])
    plt.legend()
    plt.grid()
plt.show()
plt.close()
    #plt.plot(x_df, df)

    #plt.plot(df['fruit'], df['quantity'])