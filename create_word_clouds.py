import sqlite3
from word_cloud_utils import remove_stop_words, nltk_tag_to_wordnet_tag, lemmatize_sentence, get_clues, write_word_cloud_to_file

con = sqlite3.connect('./jep.db')
cursor = con.cursor()
entity = 'ORGANIZATION'
query = "SELECT answer FROM most_common WHERE entity = '{}'".format(entity)
count = 0
for row in cursor.execute(query):
  print('LOOPING')
  count += 1
  answer = row[0]
  clues = get_clues(answer)
  write_word_cloud_to_file(answer, clues)
cursor.close()

print('TOTAL CLOUDS CREATED: {}'.format(count))

