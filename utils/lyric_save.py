"""Save new found lyrics"""
import pandas as pd
import sqlite3


def save_lyrics(song):
    columns = ['song_index', 'lyrics', 'vader', 'flair', 'combined']
    df = pd.DataFrame(song, columns=columns)

    con = sqlite3.connect("localDev.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS temp_song_sentiment (
                song_index text,
                lyrics text,
                vader real,
                flair real,
                combined real
    );""")
    
    con.commit()
    df.to_sql("temp_song_sentiment", con, if_exists="replace", index=False)
    cur.execute(f"""
        INSERT INTO song_sentiment
        SELECT * FROM temp_song_sentiment
    """)
    cur.execute(f"DROP TABLE temp_song_sentiment")
    con.commit()
