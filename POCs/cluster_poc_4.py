import sqlite3
import json

con = sqlite3.connect('../data/jep.db')
cursor = con.cursor()
answers = []
query = 'SELECT answer, COUNT(answer) AS dupes FROM answers GROUP BY answer HAVING dupes >= 23 ORDER BY dupes DESC;'
for row in cursor.execute(query):
  answers.append(row[0])
documents = {}

for idx, answer in enumerate(answers):
  print('LOOP {}'.format(idx))
  doc_string = ''
  query = 'SELECT * FROM answers WHERE answer = "{}";'.format(answer)
  for row in cursor.execute(query):
    clue = row[1]
    category = row[4]
    # category = ''
    doc = '{} {} {}'.format(category, clue, '') # Not sure whether to include the answer over and over again or not
    # doc = remove_stop_words(doc)
    # doc = lemmatize_sentence(doc)
    doc_string += ' {}'.format(doc)
  documents[answer] = {}
  documents[answer]['string'] = doc_string

with open('mc_cluster_docs.json', 'w', encoding="utf-8") as f:
  json.dump(documents, f)