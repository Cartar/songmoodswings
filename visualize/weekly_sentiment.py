import pandas as pd
import sqlite3
from datetime import datetime
from bokeh.plotting import figure
import numpy as np
from math import pi
from bokeh.models import DatetimeTickFormatter
import matplotlib.dates as mdates


# Must convert year_week back to a datetime value for plotting:

def datetime_from_yrwk(s):
    return datetime.strptime(s + '-1', '%Y%W-%w')

def weekly_sentiment_plot(datelist, region, y_data, polydeg):
    conn = sqlite3.connect('localDev.db')
    # Query for visual:
    df = pd.read_sql(f"""
        SELECT 
            year_week,
            SUM(combined * weekly_diff) AS weekly_diff_score,
            SUM(combined * inverted_rank) AS rank_score,
            SUM((combined * inverted_rank) * 2 / 3 + (combined * inverted_prev_rank) / 3) AS combined_rank_score,
            SUM(step) AS step
        FROM (
            SELECT 
                a.year || a.week AS year_week,
                101 - a.position AS inverted_rank,
                CASE WHEN a.prev_position > 0 THEN 101 - a.prev_position ELSE 0 END AS inverted_prev_rank,
                101 - a.position - (CASE WHEN a.prev_position > 0 THEN 101 - a.prev_position ELSE 0 END) AS weekly_diff,
                CASE WHEN b.combined > 0 THEN 1 WHEN b.combined < 0 THEN -1 WHEN b.combined = 0 THEN 0 END AS step,
                b.combined
            FROM {region}_chart AS a
            JOIN ( -- NOTE: only take songs with sentiment score
                SELECT song_index, combined
                FROM song_sentiment
                WHERE lyrics != '!1'
            ) as b
            ON a.song_index = b.song_index
            WHERE a.year || a.week > '{datelist[0][0] + datelist[0][1]}'
            AND a.year || a.week <= '{datelist[-1][0] + datelist[-1][1]}'
        )
        GROUP BY 1
    """, conn)

    df['date'] = df.apply (lambda row: datetime_from_yrwk(row.year_week), axis=1)

    # For whatever reason, the fit works much better like this:
    ind = df.index.to_numpy()
    model = np.poly1d(np.polyfit(
        ind,
        df[y_data],
        polydeg
    ))

    # converts ind back to the correct value!
    minimum = mdates.date2num(df['date']).min()
    refit_x = mdates.num2date(ind * 7 + minimum)

    p = figure()
    p.scatter(refit_x, df[y_data])
    p.line(refit_x, model(ind))

    # x-axis work:
    p.xaxis.formatter=DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
    p.xaxis.major_label_orientation = pi/4

    return p
