import sqlite3
from utils.word_cloud_utils import remove_stop_words, nltk_tag_to_wordnet_tag, lemmatize_sentence, get_clues, write_word_cloud_to_file

con = sqlite3.connect('./data/jep.db')
cursor = con.cursor()
entity = 'ORGANIZATION' # Edit this to grab different batches
query = 'SELECT answer FROM most_common WHERE {} = 1'.format(entity)
if not entity: 
  query = 'SELECT answer FROM most_common WHERE person = 0, organization = 0, location = 0, nne = 0;'
count = 0

for row in cursor.execute(query):
  print('LOOPING')
  count += 1
  answer = row[0]
  clues = get_clues(answer)
  write_word_cloud_to_file(answer, clues, entity)

cursor.close()
print('TOTAL CLOUDS CREATED: {}'.format(count))

