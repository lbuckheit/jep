import sqlite3
import sys
sys.path.append("..")
from utils.word_cloud_utils import remove_stop_words, nltk_tag_to_wordnet_tag, lemmatize_sentence, get_clues, write_word_cloud_to_file

con = sqlite3.connect('../data/jep.db')
cursor = con.cursor()
entity = 'organization' # Edit this to grab different batches (person, location, organization, nne)
query = 'SELECT answer FROM most_common WHERE {} = 1'.format(entity)
if not entity: 
  query = 'SELECT answer FROM most_common WHERE person IS NULL AND organization IS NULL AND location IS NULL AND nne IS NULL;'
count = 0

for row in cursor.execute(query):
  print('LOOPING')
  count += 1
  answer = row[0]
  clues = get_clues(answer)
  write_word_cloud_to_file(answer, clues, entity)

cursor.close()
print('TOTAL CLOUDS CREATED: {}'.format(count))

