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
query = 'SELECT answer FROM answers GROUP BY answer HAVING COUNT(answer) >= 23 ORDER BY COUNT(answer) DESC;'
process_string = ''
initial_insertions = []
idx = 0
total_answers = 0
for row in cursor.execute(query):
  total_answers += 1
  idx += 1
  answer = row[0]
  initial_insertions.append(answer)
  process_string += answer + ','

# Initially want to fill database with all most common answers, then we append entities where we know, then we mark whatever's left as a non-named entity
for answer in initial_insertions:
  answer = answer.replace("'", "''") # Escape single quotes for DB insert purposes
  insert_query = "INSERT INTO most_common ('answer') VALUES ('{}');".format(answer)
  cursor.execute(insert_query)
con.commit()


# print(process_string)
# Then manually process this with MonkeyLearn (https://app.monkeylearn.com/main/extractors/ex_isnnZRbS/tab/demo/) and save the results in a file somewhere

import json
from string import Template
with open('monkey_learn.json', 'r') as read_file:
    data = json.load(read_file)

extractions = data[0]['extractions']

named_entities = 0
people = 0
orgs = 0
locs = 0

for extraction in extractions:
  named_entities += 1
  answer = extraction['parsed_value']
  tag = extraction['tag_name']
  update_query = "UPDATE most_common SET entity = '{}' WHERE answer = '{}';".format(tag, answer)
  cursor.execute(update_query)
  if tag == 'PERSON':
    people += 1
  elif tag == 'COMPANY':
    orgs += 1
  elif tag == 'LOCATION':
    locs += 1
con.commit()

# An issue we run into here is when it parses an entity but doesn't match the full answer (i.e. 'Dr. Strangelove' is in the DB, but the json only has a parsed value for 'Strangelove')
fill_blank_query = "UPDATE most_common SET entity = 'NNE' WHERE entity IS NULL;"
cursor.execute(fill_blank_query)
con.commit()

cursor.close()


print('Total: {}'.format(total_answers))
print('Named Entities: {}'.format(named_entities))
print('People: {}'.format(people))
print('Organizations: {}'.format(orgs))
print('Locations: {}'.format(locs))

# Perhaps save these mappings in a table?