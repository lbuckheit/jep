import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

documents = ["This little kitty came to play when I was eating at a restaurant.",
             "Merley has the best squooshy kitten belly.",
             "Google Translate app is incredible.",
             "If you open 100 tab in google you get a smiley face.",
             "Best cat photo I've ever taken.",
             "Climbing ninja cat.",
             "Impressed with google map feedback.",
             "Key promoter extension for Google Chrome."]

con = sqlite3.connect('../data/jep.db')
cursor = con.cursor()
query = 'SELECT * FROM answers WHERE seasonid="30";'

documents = []
for index, row in enumerate(cursor.execute(query)):
  if index > 500:
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
X = vectorizer.fit_transform(documents)

true_k = 40
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

for idx, doc in enumerate(documents):
  cluster = model.labels_[idx]
  if cluster == 2:
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
#     print(terms_string)