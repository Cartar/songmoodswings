# songmoodswings

Taking inspiration from [this blog post](https://jennifer-franklin.medium.com/how-to-scrape-the-most-popular-songs-on-spotify-using-python-8a8979fa6b06), I'll start with scarpping and move from there!

## Environment:
```sh
conda create --name songmoodswings python=3.10
conda install -c conda-forge jupyterlab
pip install bs4
pip install pandas
pip install unidecode
```

## Challenges:

1. Spotify has substantially changed their code, so we'll have to use another source. https://acharts.co/ looks like a good candidate!
