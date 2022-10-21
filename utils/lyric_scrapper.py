"""Functions to scrape lyrics"""
import requests
from bs4 import BeautifulSoup
import time
from random import random
import sqlite3
import logging

from .shared import HEADER


def scrape_lyrics(top_chart):
    """Takes in the top chart and returns only new songs not found in our index"""
    new_lyrics = []

    for song in top_chart:
        song_index = song[-1]
        # Check if song lyrics are already captured:
        if not lyric_lookup(song_index):
            # try to pull lyrics:
            logging.info(f'Looking up lyrics for {song_index}')
            _, soup = azlyrics(song_index)
            lyrics = lyric_scrape(soup)
            # TODO: if lyrics are returnd as '!1', prompt user for new URL
            new_lyrics.append((song[-1], lyrics))
            time.sleep(5 * (1 + random()))

    return new_lyrics


def lyric_lookup(song_index):
    con = sqlite3.connect("localDev.db")
    cur = con.cursor()
    cur.execute(f"SELECT song_index FROM song_sentiment WHERE song_index = '{song_index}';")
    return bool(list(cur))


def azlyrics(songindex):
    lyric_url = "https://www.azlyrics.com/lyrics/" + songindex + ".html"
    
    # read page:
    read_pg = requests.get(lyric_url, headers=HEADER)
    soup = BeautifulSoup(read_pg.text, "html.parser")

    return lyric_url, soup


def lyric_scrape(soup):
    s = soup.find('div', {'class': 'col-xs-12 col-lg-8 text-center'})
    # If lyrics are found, they'll be in the 6th div:
    if s:
        lyr = s.findAll('div')
        lyrics = lyr[5].text
    else:
        lyrics = '!1'

    return lyrics
