"""Shared utility functions"""
import unidecode
from datetime import timedelta

## Pretend to be a browser (https://stackoverflow.com/questions/43590153/http-error-403-forbidden-when-reading-html/43590290#43590290):
HEADER = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

def generate_songindex(artists, song):
    first_artist = artists.split('and')[0]
    first_artist = strip_string(first_artist)
    song = strip_string(song)
    
    return first_artist + "/" + song


def strip_string(s):
    # force lower:
    s = s.lower()
    # unaccent string:
    s = unidecode.unidecode(s)
    # remove anything that isn't a letter and return
    return removeSpecialCharacter(s)


def removeSpecialCharacter(s):
    t = ""
    for i in s:
        if(i.isalpha() or i.isdigit()):
            t+=i

    return t


def create_date_list(start, end):
    datelist = [
        year_week(start)
    ]
    while start < end:
        if year_week(start) != datelist[-1]:
            datelist.append(year_week(start))
        start += timedelta(weeks=1)

    return datelist


def year_week(dateobj):
    """
    Returns the year and week of a dateobj
    """
    return (str(dateobj.isocalendar().year), str(dateobj.isocalendar().week).zfill(2))
