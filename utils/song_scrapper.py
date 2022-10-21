"""Function to scrape song list
"""
import requests
from bs4 import BeautifulSoup
from .shared import generate_songindex, HEADER

REGION = {
    "CANADA": 'https://acharts.co/canada_singles_top_100/',
    "USA": 'https://acharts.co/us_singles_top_100/',
    "UK": 'https://acharts.co/uk_singles_top_75',
    "WORLD": 'https://acharts.co/world_singles_top_40',
}

def scrape_acharts(year, week, region):
    url_base = REGION[region]
    url = url_base + year + '/' + week
    read_pg = requests.get(url, headers=HEADER)
    
    soup = BeautifulSoup(read_pg.text, "html.parser")
    
    return song_scrape(year, week, soup)


def song_scrape(year, week, soup):
    s = soup.findAll("table")[0]
    topcharts = []

    for tr in s.find("tbody").findAll("tr"):
        rank = tr.find('span', {"itemprop": "position"}).text
        rankPrev = tr.find('span', {'class':'Sub subStatsPrev'}).text
        rankPrev = rankPrev.replace("\n","").replace(" ","").strip('(').strip(')')
        title = tr.find('span', {'itemprop':'name'}).text

        artist = ""
        first = True
        for artists in tr.findAll('span', {'itemprop':'byArtist'}):
            if first:
                artist += artists.find('span', {'itemprop':'name'}).text
                first = False
            else:
                artist += " and " + artists.find('span', {'itemprop':'name'}).text
        
        songindex = generate_songindex(artist, title)
        topcharts.append((year, week, rank, rankPrev, title, artist, songindex))
    return topcharts
