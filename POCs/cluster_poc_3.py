import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.decomposition import PCA
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import json

documents = []
doc_ids = []
with open('mc_cluster_docs.json', 'r', encoding="utf-8") as f:
  doc_obj = json.load(f)
  for doc in doc_obj:
    documents.append(doc_obj[doc]['string'])
    doc_ids.append(doc)

vectorizer = TfidfVectorizer(stop_words='english')
Y = vectorizer.fit_transform(documents).todense()

true_k = 40 # 35 Seemed to work pretty well @ 2500 clues, so just trying stuff in a range around there
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=250, n_init=1)
model.fit(Y)

cluster_obj = {}
for i in range(0, true_k):
  cluster_obj[i] = { 'answers': [] }

for idx, doc_id in enumerate(doc_ids):
  cluster = model.labels_[idx]
  cluster_obj[cluster]['answers'].append(doc_id)
  # if cluster == 5:
  #   print(doc_id)

with open('cluster_poc.json', 'w', encoding="utf-8") as f:
  json.dump(cluster_obj, f)

# print("Top terms per cluster:")
# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(true_k):
#     print("Cluster %d:" % i),
#     terms_string = ''
#     for ind in order_centroids[i, :10]:
#         terms_string += terms[ind] + ', '
#     print(terms_string

