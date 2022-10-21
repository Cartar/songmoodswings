"""Scrape new songs and save for data vis"""
import argparse
from datetime import date, datetime, timedelta
import time
from random import random
import sqlite3
import logging

from utils import scrape_acharts, save_songs, scrape_lyrics, save_lyrics, calc_sentiment, create_date_list

def main(datelist, region):
    logging.basicConfig(filename='run_song_scrapper.log', level=logging.INFO)
    logging.info(f'Started scrapping for region: {region}')
    # Loop the weeks to scrape:
    for year, week in datelist:
        logging.info(f'Scrapping week: {week}, year: {year}')
        top_chart = scrape_acharts(year, week, region)
        
        save_songs(top_chart, region)

        # Scrape lyrics only returns new song lyrics not already saved
        new_lyrics = scrape_lyrics(top_chart)

        # For new songs, calculate sentiment and save:
        for song_index, lyrics in new_lyrics:
            vader, flair = calc_sentiment(lyrics)
            song = [
                (
                    song_index,
                    lyrics,
                    vader,
                    flair,
                    (vader*2 + flair/2) / 3 # See discussion in compare notebook
                )
            ]
            save_lyrics(song)

        time.sleep(2 * (1 + random()))
    
    logging.info('Finished')


if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument('--startdt', help='Start date to scrape from. Format: %Y%m%d. Default is 1 week ago.')
    parser.add_argument('--enddt', help='End date to scrape from. Format: %Y%m%d. Default is today.')
    parser.add_argument('--region', help='Region to scrape from. Default is CANADA. Options include: CANADA, UK, USA, and WORLD')
    args = parser.parse_args()
    
    # Create time range to loop through, and region:
    if args.startdt:
        startdt = datetime.strptime(args.startdt, '%Y%m%d')
    else:
        d = date.today()
        startdt = datetime(d.year, d.month, d.day)
        startdt -= timedelta(weeks=1)

    if args.enddt:
        enddt = datetime.strptime(args.enddt, '%Y%m%d')
    else:
        d = date.today()
        enddt = datetime(d.year, d.month, d.day)
    
    if args.region:
        region = args.region
    else:
        region = 'CANADA'

    # Create necessary databases if they don't already exist:
    con = sqlite3.connect("localDev.db")
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {region}_chart (
                year text,
                week text,
                position integer,
                prev_position integer,
                song text,
                artist text,
                song_index text
    );""")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS song_sentiment (
                song_index text,
                lyrics text,
                vader real,
                flair real,
                combined real
    );""")
    con.commit()

    datelist = create_date_list(startdt, enddt)
    main(datelist, region)
    