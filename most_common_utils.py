import sqlite3
import json
import re
from string import Template

# Getting the list of most common answers for API processing and initial DB populations
def get_most_common():
  con = sqlite3.connect('./jep.db')
  cursor = con.cursor()
  # My arbitrary threshold for which answers to include is a min. of one occurance per season (23 seasons in the DB)
  query = 'SELECT answer FROM answers GROUP BY answer HAVING COUNT(answer) >= 23 ORDER BY COUNT(answer) DESC;'
  api_string = ''
  initial_insertions = []
  idx = 0
  total_answers = 0

  for row in cursor.execute(query):
    total_answers += 1
    idx += 1
    answer = row[0]
    initial_insertions.append(answer)
    api_string += answer + ','
  
  cursor.close()
  return { 'api_string': api_string, 'initial_insertions': initial_insertions }

# For filling the DB with every answer, because the API results will ignore NNEs (e.g. hydrogen, blue, 7)
def initially_populate_table(initial_insertions):
  con = sqlite3.connect('./jep.db')
  cursor = con.cursor()
  for answer in initial_insertions:
    answer = answer.replace("'", "''") # Escape single quotes for DB insert purposes
    answer = answer.replace('\\', '')
    insert_query = "INSERT INTO most_common ('answer') VALUES ('{}');".format(answer)
    cursor.execute(insert_query)
  con.commit()
  cursor.close()

# For assigining the entity columns in the DB
def process_api_response():
  con = sqlite3.connect('./jep.db')
  cursor = con.cursor()
  with open('monkey_learn.json', 'r') as read_file:
    data = json.load(read_file)
  extractions = data[0]['extractions']

  for extraction in extractions:
    answer = extraction['parsed_value']
    tag = extraction['tag_name']
    if tag == 'COMPANY':
      tag = 'ORGANIZATION'
    update_query = "UPDATE most_common SET {} = 1 WHERE answer = '{}';".format(tag, answer)
    cursor.execute(update_query)

  con.commit()
  cursor.close()

# For doing manual updates of the entities where the NER is lacking
def update_entity_columns():
  # *** These required updates were determined from manual review of the entries***

  # LOCATION SHOULD ALSO be PERSON: Venus, St. Paul, Medea
  # LOCATION SHOULD ONLY be PERSON: Orson Welles, Teddy Roosevelt, Hercules, Dracula, Churchill, Florence Nightengale, Gweneth Paltrow, Merlin
  # LOCATION SHOULD ALSO be ORGANIZATION: Amazon
  # LOCATION SHOULD ONLY be UNCATEGORIZED: West Side Story, Wurthering Heights, Beowulf, Lolita, Swan Lake, Bambi

  # PERSON SHOULD ONLY be UNCATEGORIZED: Aerosmith, Gladiator
  # PERSON SHOULD ALSO be ORGANIZATION: Duke

  # ORGANIZATION SHOULD ONLY be PERSON: Lincoln, Galileo, Rembrandt, Brigham Young, Columbus, Edison, Voltaire, Eminem, Orion, Monet, King Kong, Athena, Tolkien, MacArthur, Odysseus, Magellan, Hermes, LBJ, Goya, Stuart Little, Pegasus, Marconi
  # ORGANIZATION SHOULD ALSO be PERSON: Stanford
  # ORGANIZATION SHOULD ONLY be LOCATION: Monaco, Niagara Falls, Westminster Abbey, Canterbury, Valley Forge, American Samoa
  # ORGANIZATION SHOULD ALSO be LOCATION: Liverpool, Plymouth
  # ORGANIZATION SHOULD ONLY be UNCATEGORIZED: ABBA, Islam, East of Eden, Brave New World, Animal House, Wings, Star Trek, 

  con = sqlite3.connect('./jep.db')
  cursor = con.cursor()

  # First want to set NNEs with the heuristic that single letters and words with no capital letters are probably NNEs
  unset_entities_query = 'SELECT * FROM most_common WHERE person IS NULL AND organization IS NULL and location IS NULL;'
  cursor.execute(unset_entities_query)
  unset_entities = cursor.fetchall()
  nne_regex = re.compile(r'[A-Z]')

  for answer in unset_entities:
    answer = answer[0]
    if len(answer) == 1 or not nne_regex.search(answer):
      update_query = 'UPDATE most_common SET nne = 1 WHERE answer = "{}"'.format(answer)
      cursor.execute(update_query)
  con.commit()

  # Next update the LOCATIONs
  loc_to_person = ['Orson Welles', 'Teddy Roosevelt', 'Hercules', 'Dracula', 'Churchill', 'Florence Nightengale', 'Gweneth Paltrow', 'Merlin']
  loc_also_person = ['Venus', 'St. Paul']
  loc_also_org = ['Amazon']
  loc_to_uncat = ['West Side Story', 'Wurthering Heights', 'Beowulf', 'Lolita', 'Swan Lake', 'Bambi']

  for answer in loc_to_person:
    update_query = 'UPDATE most_common SET person = 1, location = 0 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in loc_also_person:
    update_query = 'UPDATE most_common SET person = 1 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in loc_also_org:
    update_query = 'UPDATE most_common SET organization = 1 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in loc_to_uncat:
    update_query = 'UPDATE most_common SET location = 0 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  # Next update the PERSONs
  person_to_uncat = ['Aerosmith', 'Gladiator']
  person_also_org = ['Duke']
  for answer in person_to_uncat:
    update_query = 'UPDATE most_common SET person = 0 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in person_also_org:
    update_query = 'UPDATE most_common SET organization = 1 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  # Next update the ORGANIZATIONs
  org_to_person = ['Lincoln', 'Galileo', 'Rembrandt', 'Brigham Young', 'Columbus', 'Edison', 'Voltaire', 'Eminem', 'Orion', 'Monet', 'King Kong', 'Athena', 'Tolkien', 'MacArthur', 'Odysseus', 'Magellan', 'Hermes', 'LBJ', 'Goya', 'Stuart Little', 'Pegasus', 'Marconi']
  org_also_person = ['Stanford']
  org_to_loc = ['Monaco', 'Niagara Falls', 'Westminster Abbey', 'Canterbury', 'Valley Forge', 'American Samoa']
  org_also_loc = ['Liverpool', 'Plymouth']
  org_to_uncat = ['ABBA', 'Islam', 'East of Eden', 'Brave New World', 'Animal House', 'Wings', 'Star Trek', 'R.E.M.']

  for answer in org_to_person:
    update_query = 'UPDATE most_common SET organization = 0, person = 1 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in org_also_person:
    update_query = 'UPDATE most_common SET person = 1 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in org_to_loc:
    update_query = 'UPDATE most_common SET organization = 0, location = 1 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in org_also_loc:
    update_query = 'UPDATE most_common SET location = 1 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  for answer in org_to_uncat:
    update_query = 'UPDATE most_common SET organization = 0 WHERE answer = "{}"'.format(answer)
    cursor.execute(update_query)

  con.commit()
  cursor.close()
