import time
from get_season_games import get_season_games
from scrape_game import scrape_game

# Goal is to get seasons 14-Present (J! Archive starts to miss 20+ episodes per season from 1-13, so I think those are less helpful and they're also so old that they're not as relevant)
# Seasons scraped: 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, GOAT
# Seasons fully TODO: 37 (once it's complete)
# Partial scrapes: 35 (Tournament game breaking things)
# Missing games: S25URL3063 (Unclear issue w/ soup but isolated to this game), S35URL6227 (Tournament game)

# Edit this to scrape different seasons
season = 35

games = get_season_games(season)

for index, game in enumerate(games):
  print('SCRAPING GAME ' + game)
  print('LOOP ITERATION: ' + str(index + 1))
  scrape_game(game, season)
  print('GAME SCRAPED - WAITING 10 SECONDS')
  time.sleep(10)