# songmoodswings

Taking inspiration from [this blog post](https://jennifer-franklin.medium.com/how-to-scrape-the-most-popular-songs-on-spotify-using-python-8a8979fa6b06), I'll start with scarpping and move from there!

## Environment:
```sh
conda create --name songmoodswings python=3.9 -y
conda activate songmoodswings
conda install -c conda-forge jupyterlab -y
pip install bs4
pip install pandas
pip install unidecode
pip install flair
pip install vaderSentiment # THIS OVER FLAIR?

jupyter lab
```

## Challenges:

1. Spotify has substantially changed their code, so we'll have to use another source. https://acharts.co/ looks like a good candidate!
2. azlyrics is inconsistent with how it indexes songs.
    * Two ways around this: i) use another site; ii) manually find the songs that my code missed.


## process:

1. Extract top 100 songs for each week in 2020 in Canada.
2. Populate lyrics for as many songs as possible (determine failure rate and why).
3. Run sentiment analysis for all lyrics obtained.

## Next steps:

1. Train my own sentiment analysis using [BERT](https://www.kaggle.com/code/prakharrathi25/sentiment-analysis-using-bert/notebook)

## Appendix:

Scrapping song lyrics could alternatively be done via https://github.com/jasonqng/genius-lyrics-search.

A fun into to [flair](https://github.com/flairNLP/flair) is [here](https://www.analyticsvidhya.com/blog/2019/02/flair-nlp-library-python/).
