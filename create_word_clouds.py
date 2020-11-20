import sqlite3
from word_cloud_utils import remove_stop_words, nltk_tag_to_wordnet_tag, lemmatize_sentence, get_clues, write_word_cloud_to_file

con = sqlite3.connect('./jep.db')
cursor = con.cursor()
threshold = 100
query = 'SELECT answer FROM answers GROUP BY answer HAVING COUNT(answer) > ' + str(threshold) + ' ORDER BY COUNT(answer) DESC;'
for row in cursor.execute(query):
  answer = row[0]
  clues = get_clues(answer)
  write_word_cloud_to_file(answer, clues)
cursor.close()

