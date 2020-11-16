# TODO - Here's where the loop that scrapes each game in sequence will live
# TODO - Perhaps scraping on a season-by-season basis is the best way to break it out
import time
from getSeasonGames import getSeasonGames
from gameScraper import scrapeGame

# Edit this to scrape different seasons
season = 20

games = getSeasonGames(season)

for index, game in enumerate(games):
  print('INITIALIZING LOOP')
  print(index)
  if (index > 10):
    break
  scrapeGame(game, season)
  print('GOING TO SLEEP')
  time.sleep(10)