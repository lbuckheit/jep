import time
from getSeasonGames import getSeasonGames
from gameScraper import scrapeGame

# Edit this to scrape different seasons
season = 20

games = getSeasonGames(season)

for index, game in enumerate(games):
  print('SCRAPING GAME')
  print(index)
  scrapeGame(game, season)
  print('GAME SCRAPED - WAITING 15 SECONDS')
  time.sleep(15)