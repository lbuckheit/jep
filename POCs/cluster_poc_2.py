import sqlite3
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.decomposition import PCA

from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np

con = sqlite3.connect('../data/jep.db')
cursor = con.cursor()
query = 'SELECT * FROM answers WHERE seasonid="30";'

documents = []
for index, row in enumerate(cursor.execute(query)):
  if index > 6000:
    break

  answer = row[0]
  clue = row[1]
  category = row[4]
  # category = ''
  doc = '{} {} {}'.format(category, clue, answer)
  # doc = remove_stop_words(doc)
  # doc = lemmatize_sentence(doc)
  documents.append(doc)

vectorizer = TfidfVectorizer(stop_words='english')
Y = vectorizer.fit_transform(documents).todense()

# **** THIS PORTION IS USED TO DETERMINE HOW MANY CLUSTERS BASED ON VISUAL OBSERVATION OF THE ELBOW GRAPH.  THEN YOU PLUG IN THE SELECTED VALUE AS true_k ****
# pca = PCA(n_components=2).fit(Y)
# data2D = pca.transform(Y)
# # plt.scatter(data2D[:,0], data2D[:,1], c='blue')
# # plt.show()    

# x1 = data2D[:,0]
# x2 = data2D[:,1]

# plt.plot()
# # plt.xlim([0, 10])
# # plt.ylim([0, 10])
# plt.title('Dataset')
# plt.scatter(x1, x2)
# plt.show()

# # create new plot and data
# plt.plot()
# X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
# colors = ['b', 'g', 'r']
# markers = ['o', 'v', 's']

# # k means determine k
# distortions = []
# K = range(10,100)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k).fit(X)
#     kmeanModel.fit(X)
#     distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# # Plot the elbow
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Distortion')
# plt.title('The Elbow Method showing the optimal k')
# plt.show()

true_k = 40 # 35 Seemed to work pretty well @ 2500 clues
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(Y)

for idx, doc in enumerate(documents):
  cluster = model.labels_[idx]
  if cluster == 1:
    print(doc)
  # print(documents[idx])
  # print(model.labels_[idx])

# print("Top terms per cluster:")
# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(true_k):
#     print("Cluster %d:" % i),
#     terms_string = ''
#     for ind in order_centroids[i, :10]:
#         terms_string += terms[ind] + ', '
#     print(terms_string

