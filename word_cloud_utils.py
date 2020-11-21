# Sentence lemmataztion from by https://medium.com/@gaurav5430/using-nltk-for-lemmatizing-sentences-c1bfff963258
# Various nltk and wordcloud tutorials from geeksforgeeks.com

import sqlite3
import nltk
import string
import re
import matplotlib.pyplot as plt 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from wordcloud import WordCloud

def remove_stop_words(sentence):
  stop_words = set(stopwords.words('english'))
  word_tokens = nltk.word_tokenize(sentence)
  filtered_sentence = [w for w in word_tokens if not w in stop_words]
  filtered_sentence = []
  for w in word_tokens: 
    if w not in stop_words: 
      filtered_sentence.append(w)  

  return ' '.join(filtered_sentence)

def nltk_tag_to_wordnet_tag(nltk_tag):
  if nltk_tag.startswith('J'):
    return wordnet.ADJ
  elif nltk_tag.startswith('V'):
    return wordnet.VERB
  elif nltk_tag.startswith('N'):
    return wordnet.NOUN
  elif nltk_tag.startswith('R'):
    return wordnet.ADV
  else:          
    return None

def lemmatize_sentence(sentence):
  lemmatizer = WordNetLemmatizer()
  # Tokenize the sentence and find the POS tag for each token
  nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
  # Tuple of (token, wordnet_tag)
  wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
  lemmatized_sentence = []
  for word, tag in wordnet_tagged:
    if tag is None:
      # If there is no available tag, append the token as is
      lemmatized_sentence.append(word)
    else:        
      # Else use the tag to lemmatize the token
      lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))

  return ' '.join(lemmatized_sentence)

def get_clues(answer):
  con = sqlite3.connect('./jep.db')
  cursor = con.cursor()
  query = 'SELECT * FROM answers WHERE answer="' + answer + '"'
  clues = []
  for row in cursor.execute(query):
    clues.append(row[1])

  # Capturing the "only last name required" nature of Jeopardy clues
  # This isn't a perfect method, and will capture some false positives, but it should nonetheless be helpful
  split_answer = answer.split(' ')
  words_in_answer = len(split_answer)
  if words_in_answer > 1:
    alternate_answer = split_answer[-1]
    query = 'SELECT * FROM answers WHERE answer="' + alternate_answer + '"'
    for row in cursor.execute(query):
      clues.append(row[1])
  cursor.close()
  
  return clues

def merge_clues(clues):
  word_cloud_words = ''
  for clue in clues:
    clue = clue.lower()
    clue = remove_stop_words(clue)
    clue = lemmatize_sentence(clue)
    clue += ' ' # Gotta add a space after each complete clue so the words don't run together
    clue = clue.replace("'s", '') # Removing posessive esses that get left by the filtering
    word_cloud_words += clue

  return word_cloud_words

def write_word_cloud_to_file(answer, clues):
  words = merge_clues(clues)
  wordcloud = WordCloud(width = 800, height = 800, background_color = 'white', min_font_size = 10).generate(words) 
  plt.figure(figsize = (8, 8), facecolor = None) 
  plt.imshow(wordcloud) 
  plt.axis('off') 
  title = answer + ' | n = ' + str(len(clues))
  plt.title(title, fontsize = 50)
  plt.tight_layout(pad = 0) 
  plt.savefig('./word_clouds/' + answer + '.png')