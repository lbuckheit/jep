import urllib.request
from bs4 import BeautifulSoup
import re

def get_season_games(season):
  base_URL = 'https://j-archive.com/showseason.php?season='
  scrape_URL = base_URL + str(season)
  page = urllib.request.urlopen(scrape_URL)
  soup = BeautifulSoup(page.read(), 'lxml')
  games = []
  links = soup.find_all('a')
  game_regex = re.compile(r'http:\/\/www\.j-archive\.com\/showgame\.php\?game_id=(\d+)')
  for link in links:
    href = link['href']
    game_match = game_regex.match(href)
    if game_match:
      games.append(game_match.group(1))
  return games