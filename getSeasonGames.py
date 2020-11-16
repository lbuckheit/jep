import urllib.request
from bs4 import BeautifulSoup
import re

def getSeasonGames(season):
  baseURL = 'https://j-archive.com/showseason.php?season='
  scrapeURL = baseURL + str(season)
  page = urllib.request.urlopen(scrapeURL)
  soup = BeautifulSoup(page.read(), 'lxml')
  games = []
  links = soup.find_all('a')
  gameRegex = re.compile(r'http:\/\/www\.j-archive\.com\/showgame\.php\?game_id=(\d+)')
  for link in links:
    href = link['href']
    gameMatch = gameRegex.match(href)
    if gameMatch:
      games.append(gameMatch.group(1))
  return(games)