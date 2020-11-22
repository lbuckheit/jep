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

import sqlite3
import re

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
loc_to_person = ['Venus', 'St. Paul', 'Medea']
loc_also_person = ['Orson Welles', 'Teddy Roosevelt', 'Hercules', 'Dracula', 'Churchill', 'Florence Nightengale', 'Gweneth Paltrow', 'Merlin']
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
for answer in loc_also_person:
  update_query = 'UPDATE most_common SET person = 0 WHERE answer = "{}"'.format(answer)
  cursor.execute(update_query)

for answer in loc_also_person:
  update_query = 'UPDATE most_common SET organization = 1 WHERE answer = "{}"'.format(answer)
  cursor.execute(update_query)

# Next update the ORGANIZATIONs
org_to_person = ['Lincoln', 'Galileo', 'Rembrandt', 'Brigham Young', 'Columbus', 'Edison', 'Voltaire', 'Eminem', 'Orion', 'Monet', 'King Kong', 'Athena', 'Tolkien', 'MacArthur', 'Odysseus', 'Magellan', 'Hermes', 'LBJ', 'Goya', 'Stuart Little', 'Pegasus', 'Marconi']
org_also_person = ['Stanford']
org_to_loc = ['Monaco', 'Niagara Falls', 'Westminster Abbey', 'Canterbury', 'Valley Forge', 'American Samoa']
org_also_loc = ['Liverpool', 'Plymouth']
org_to_uncat = ['ABBA', 'Islam', 'East of Eden', 'Brave New World', 'Animal House', 'Wings', 'Star Trek']

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