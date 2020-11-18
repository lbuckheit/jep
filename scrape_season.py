import time
from get_season_games import get_season_games
from scrape_game import scrape_game

# Seasons scraped: 20, 21, 22, 23, 24, 25
# Missing games: S25URL3063
# Edit this to scrape different seasons
season = 25

games = get_season_games(season)

for index, game in enumerate(games):
  print('SCRAPING GAME ' + game)
  print('LOOP ITERATION: ' + str(index + 1))
  scrape_game(game, season)
  print('GAME SCRAPED - WAITING 10 SECONDS')
  time.sleep(10)