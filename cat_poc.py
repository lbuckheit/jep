# https://medium.com/analytics-vidhya/basics-of-using-pre-trained-glove-vectors-in-python-d38905f356db
# https://github.com/wsuh60/nlp_jeopardy
# Named Entity Recognition
# https://www.aclweb.org/anthology/W15-1830.pdf
# https://patents.google.com/patent/US20080071519

# Ideas
# Could first break into named entities and not
# Then can run word2vec on the non named entities to cluster
# Clustering the named entities is tougher, but they might be broken down enough that manual is practical

# Notes
# Gonna scrape the MonkeyLearn API for NER
# Works of art are a notable weakness here

import sqlite3

con = sqlite3.connect('./jep.db')
cursor = con.cursor()
query = 'SELECT answer FROM answers GROUP BY answer HAVING COUNT(answer) >= 45 AND COUNT(answer) <= 60 ORDER BY COUNT(answer) DESC;'
process_string = ''
idx = 0
for row in cursor.execute(query):
  idx += 1
  answer = row[0]
  process_string += answer + ','
cursor.close()

# print(process_string)
# Then manually process this with MonkeyLearn (https://app.monkeylearn.com/main/extractors/ex_isnnZRbS/tab/demo/) and save the results in a file somewhere

import json
with open('monkey_learn.json', 'r') as read_file:
    data = json.load(read_file)

extractions = data[0]['extractions']

people = 0
orgs = 0
locs = 0

for extraction in extractions:
  tag = extraction['tag_name']
  if tag == 'PERSON':
    people += 1
  elif tag == 'COMPANY':
    orgs += 1
  elif tag == 'LOCATION':
    locs += 1

print(people)
print(orgs)
print(locs)

# Perhaps save these mappings in a table?