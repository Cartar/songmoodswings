import streamlit as st
from datetime import datetime
from utils import create_date_list
from visualize import weekly_sentiment_plot, song_list_df

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

st.title("Song Sentiment")

st.write("Using [acharts](https://acharts.co/), we've collected the top hits from Canada, the US, UK, and around the world.")
st.write("""
Up to 80% of song lyrics are scrapped from [azlyrics](https://www.azlyrics.com/), which have a positive or negative
sentiment score calculated using a combination of VADER and Flair's built in sentiment analysis.
""")
st.write("Let's check out some of the data now.")

startdate = st.text_input("Starting date, formatted YYYYMMDD. Minimum: 20180101")
enddate = st.text_input("End date, formatted YYYYMMDD.")

# Step 1: define start end end period:

if startdate:
    startdate = datetime.strptime(startdate, '%Y%m%d')
else:
    startdate = datetime.strptime('20180101', '%Y%m%d')
if enddate:
    enddate = datetime.strptime(enddate, '%Y%m%d') 
else:
    enddate = datetime.strptime('20220101', '%Y%m%d')

datelist = create_date_list(startdate, enddate)

# select box in sidebar demo
df = pd.DataFrame(
    {
        "region": ['CANADA', 'USA', 'UK', 'WORLD'],
        "sentiment score": ['weekly_diff_score',
                            'rank_score',
                            'combined_rank_score',
                            'step'],
        "polyfit degree": [4, 8, 16, 32]
    }
)
region = st.sidebar.selectbox("Which region do you want to see?", df["region"])
score_type = st.sidebar.selectbox("What sentiment score type do you want to visualize?", df["sentiment score"])
polydeg = st.sidebar.selectbox("How many degrees should the polyfit curve have?", df["polyfit degree"])

st.header("Data selected")
"You selected:", region
"scored by:", score_type
"fit by:", polydeg
"over the date range:", startdate, "to", enddate


# Step 3: pull data
st.header("Charts")

p = weekly_sentiment_plot(
    datelist=datelist,
    region=region,
    y_data=score_type,
    polydeg=polydeg)
st.bokeh_chart(p, use_container_width=True)


df = song_list_df(datelist, region)

if st.checkbox("Show dataframe"):
    st.dataframe(df)

left_column, right_column = st.columns(2)
pressed = left_column.button("Like what you see?")
if pressed:
    right_column.write("Thanks!")
    st.balloons()

expander = st.expander("FAQ")
expander.write("Work in progress...")
