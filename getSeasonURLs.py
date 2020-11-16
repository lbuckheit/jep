import urllib.request
from bs4 import BeautifulSoup
import re

def getSeasonURLs(season):
  baseURL = 'https://j-archive.com/showseason.php?season='
  scrapeURL = baseURL + str(season)
  page = urllib.request.urlopen(scrapeURL)
  soup = BeautifulSoup(page.read(), 'lxml')
  gameURLs = []
  links = soup.find_all('a')
  gameRegex = re.compile(r'http:\/\/www\.j-archive\.com\/showgame\.php\?game_id=\d+')
  for link in links:
    href = link['href']
    if gameRegex.match(href):
      gameURLs.append(href)
  return(gameURLs)


getSeasonURLs(20)

