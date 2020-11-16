import time
from getSeasonGames import getSeasonGames
from gameScraper import scrapeGame

# Seasons scraped: 20, 21
# Edit this to scrape different seasons
season = 21

games = getSeasonGames(season)

for index, game in enumerate(games):
  print('SCRAPING GAME')
  print(index)
  scrapeGame(game, season)
  print('GAME SCRAPED - WAITING 10 SECONDS')
  time.sleep(10)