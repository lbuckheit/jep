# https://medium.com/analytics-vidhya/basics-of-using-pre-trained-glove-vectors-in-python-d38905f356db
# https://github.com/wsuh60/nlp_jeopardy
# Named Entity Recognition
# https://www.aclweb.org/anthology/W15-1830.pdf

# Ideas
# Could first break into named entities and not
# Then can run word2vec on the non named entities to cluster
# Clustering the named entities is tougher, but they might be broken down enough that manual is practical

import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

embeddings_dict = {}
with open('/training_data/glove.6B.50d.txt', 'r', encoding='utf-8') as f:
  for line in f:
    values = line.split()
    word = values[0]
    vector = np.asarray(values[1:], "float32")
    embeddings_dict[word] = vector