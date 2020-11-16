# TODO - Here's where the loop that scrapes each game in sequence will live
# TODO - Perhaps scraping on a season-by-season basis is the best way to break it out
import time

from gameScraper import scrapeGame

games = ['http://www.j-archive.com/showgame.php?game_id=2730', 'http://www.j-archive.com/showgame.php?game_id=2731', 'http://www.j-archive.com/showgame.php?game_id=2732']

for game in games:
  print('INITIALIZING LOOP')
  scrapeGame(game)
  print('GOING TO SLEEP')
  time.sleep(5)