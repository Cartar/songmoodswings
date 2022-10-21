"""Save top songs in SQLite database"""
import pandas as pd
import sqlite3

def save_songs(top_chart, region):
    columns = ['year', 'week', 'position', 'prev_position', 'song', 'artist', 'song_index']
    chart_df = pd.DataFrame(top_chart, columns=columns)

    ## Clean up data (get types correct, and prev_position "new" etc.)
    chart_df.loc[chart_df['prev_position'] == 'new', 'prev_position'] = 0
    chart_df.loc[chart_df['prev_position'] == 're-entry', 'prev_position'] = 0
    chart_df = chart_df.astype({'position': 'int32', 'prev_position': 'int32'})

    ## Next up, need to put that in SQLite db
    con = sqlite3.connect("localDev.db")
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS temp_{region}_chart (
                year text,
                week text,
                position integer,
                prev_position integer,
                song text,
                artist text,
                song_index text
    );""")
    con.commit()

    chart_df.to_sql(f"temp_{region}_chart", con, if_exists="replace", index=False)
    cur.execute(f"""
        INSERT INTO {region}_chart
        SELECT * FROM temp_{region}_chart
        WHERE (year, week) NOT IN (SELECT year, week FROM {region}_chart GROUP BY 1,2)
    """)
    cur.execute(f"DROP TABLE temp_{region}_chart")
    con.commit()
