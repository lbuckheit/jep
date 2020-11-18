import urllib.request
from bs4 import BeautifulSoup
import re
import sqlite3

# Master project TODOs
# TODO - Try/catch or equivalent so a failed scrape doesn't break the loop (MED-HARD) (Perhaps not really necessary if you're just scraping on a season-by-season basis)
# TODO - Log failures to avoid re-scraping as much as possible (MED-HARD) (See above)
# TODO - NLP to group answers (MED-HARD) (Word2Vec, GloVe, https://www.kylepoole.me/blog/20200912_Wikipedia_Quiz/)
# TODO - Word cloud master loop (MED-HARD)
# TODO - Break some of these functions out into other files?
# TODO - Handle quotes in answers? (which I guess happens when Alex has to say the answer after a triple stumper?) (See "On, Wisconsin", game S25URL3070)

# Scraping-specific TODOs
# TODO - Parenthetical/abbreviations/nicknames/etc. Handling? (LATER)
# TODO - Do I need all these re.complie lines?

# Mapping board positions to dollar values
value_obj = {
  1: 200,
  2: 400,
  3: 600,
  4: 800,
  5: 1000
}

def scrape_game(game, season):
  game_ID = str(game)
  season_ID = str(season)
  base_URL = 'http://www.j-archive.com/showgame.php?game_id='
  game_URL = base_URL + str(game)
  page = urllib.request.urlopen(game_URL)
  soup = BeautifulSoup(page.read(), 'lxml')
  game_object = {}

  # Categories
  categories = {
    'J': {},
    'DJ': {},
    'FJ': {}
  }
  j = soup.find(id='jeopardy_round')
  for idx, elem in enumerate(j.findAll(class_='category_name')):
    categories['J'][idx + 1] = elem.text
  dj = soup.find(id='double_jeopardy_round')
  for idx, elem in enumerate(dj.findAll(class_='category_name')):
    categories['DJ'][idx + 1] = elem.text
  fj = soup.find(id='final_jeopardy_round')
  for idx, elem in enumerate(fj.findAll(class_='category_name')):
    categories['FJ'][idx + 1] = elem.text

  # Clues/Segments/Values/Etc.
  for elem in soup.findAll(class_='clue_text'):
    clue = elem.text

    raw_position = elem['id']
    position = raw_position.split('clue_')[1]

    split_position = position.split('_')
    segment = split_position[0]
    if (segment == 'TB'): # Very occasionally games will have tiebreaker questions.  For my purposes I will just consider them a second Final Jeopardy clue
      value = 0
      category = categories['FJ'][1]
    elif (segment == 'FJ'):
      value = 0
      category = categories['FJ'][1]
    else:
      board_X_Position = int(split_position[1])
      board_Y_Position = int(split_position[2])
      value = value_obj[board_Y_Position]
      if (segment == 'DJ'):
        value *= 2
      category = categories[segment][board_X_Position]

    game_object[position] = {}
    game_object[position]['clue'] = clue
    game_object[position]['position'] = position
    game_object[position]['segment'] = segment
    game_object[position]['value'] = value
    game_object[position]['category'] = category

  # Answers
  for elem in soup.findAll(onmouseover=True):
    search_string = elem['onmouseover']

    position_regex = re.compile(r'clue_[TBDFJ_123456789]+')
    raw_position = position_regex.search(search_string)
    position = raw_position.group(0).split('clue_')[1]

    answer_regex = re.compile(r'<em class=\\?"correct_response\\?">(.*?)<\/em>')
    raw_answer = answer_regex.search(search_string)
    answer = raw_answer.group(1)
    # Stripping the italic tags out of certain answers
    answer = answer.replace('<i>', '')
    answer = answer.replace('</i>', '')

    game_object[position]['answer'] = answer

  # Database Entry
  con = sqlite3.connect('./jep.db')
  cursor = con.cursor()
  for position in game_object:
    answer = game_object[position]['answer']
    answer = answer.replace("'", "''") # Escape single quotes for DB insert purposes

    clue = game_object[position]['clue']
    clue = clue.replace("'", "''")

    segment = game_object[position]['segment']
    segment = segment.replace("'", "''")

    value = str(game_object[position]['value'])

    category = game_object[position]['category']
    category = category.replace("'", "''")

    update_insert = "INSERT INTO answers ('answer', 'clue', 'segment', 'value', 'category', 'gameid', 'seasonid') "
    update_values = "VALUES ('" + answer + "', '" + clue + "', '" + segment + "', '" + value + "', '" + category + "', '" + game_ID + "', '" + season_ID + "');"
    update_query = update_insert + update_values
    cursor.execute(update_query)
  con.commit()
  cursor.close()