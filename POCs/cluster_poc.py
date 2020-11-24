# Used code from:
# https://pythonprogramminglanguage.com/kmeans-text-clustering/
# https://pythonprogramminglanguage.com/kmeans-elbow-method/
# https://stackoverflow.com/questions/28160335/plot-a-document-tfidf-2d-graph

# Helpful links (no code yet)
# https://stackoverflow.com/questions/53663675/doc2vec-clustering-with-kmeans-for-a-new-document
# https://radimrehurek.com/gensim/models/doc2vec.html
# https://github.com/aniketbote/Document-Clustering-Doc2vec/blob/master/Clustering/Clustering_code_Doc2Vec/clustering_Documents_Doc2Vec.py
# https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html
# https://towardsdatascience.com/detecting-document-similarity-with-doc2vec-f8289a9a7db7
# https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsworkingpaperseriesnumber14unsuperviseddocumentclusteringwithclustertopicidentification


import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import sys
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
sys.path.append("..")
from utils.word_cloud_utils import remove_stop_words, lemmatize_sentence

con = sqlite3.connect('../data/jep.db')
cursor = con.cursor()
query = 'SELECT * FROM answers WHERE seasonid="30";'

documents = []
for index, row in enumerate(cursor.execute(query)):
  if index > 60:
    break

  answer = row[0]
  clue = row[1]
  category = row[4]
  doc = '{} {} {}'.format(category, clue, answer)
  doc = remove_stop_words(doc)
  doc = lemmatize_sentence(doc)
  documents.append(doc)

# t_vectorizer = TfidfVectorizer()
t_vectorizer = TfidfTransformer()
c_vectorizer = CountVectorizer()

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
]) 

X = pipeline.fit_transform(documents).todense()
# print(X)

pca = PCA(n_components=2).fit(X)
data2D = pca.transform(X)
# plt.scatter(data2D[:,0], data2D[:,1], c='blue')
# plt.show()

true_k = 12
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)
clusters = model.labels_.tolist()

print(model.labels_)

plt.scatter(data2D[:,0], data2D[:,1], c=clusters)
plt.show()

# distortions = []
# K = range(25,50)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k).fit(X)
#     kmeanModel.fit(X)
#     distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# print(distortions)

# true_k = 2
# model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
# model.fit(X)

# print("Top terms per cluster:")
# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(true_k):
#     print("Cluster %d:" % i),
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind]),
#     print

# print("\n")
# print("Prediction")

# Y = vectorizer.transform(["chrome browser to open."])
# prediction = model.predict(Y)
# print(prediction)

# Y = vectorizer.transform(["My cat is hungry."])
# prediction = model.predict(Y)
# print(prediction)