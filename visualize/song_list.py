import pandas as pd
import sqlite3

def song_list_df(datelist, region):
    conn = sqlite3.connect('localDev.db')
    df = pd.read_sql(f"""
        SELECT
            a.song
            , a.artist
            , a.position
            , a.prev_position
            , b.combined
            , a.week
            , a.year
        FROM {region}_chart AS a
        LEFT JOIN (
            SELECT song_index, combined
            FROM song_sentiment
            WHERE lyrics != '!1'
        ) as b
        ON a.song_index = b.song_index
        WHERE a.year || a.week > '{datelist[0][0] + datelist[0][1]}'
        AND a.year || a.week <= '{datelist[-1][0] + datelist[-1][1]}';
    """, conn)

    return df
