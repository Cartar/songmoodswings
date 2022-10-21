"""Functions for calculating sentiment anylsis"""
import torch
from flair.models import TextClassifier
from flair.data import Sentence
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import unidecode


VADER = SentimentIntensityAnalyzer()
FLAIR = TextClassifier.load('sentiment')


def calc_sentiment(lyrics):
    """returns a tupple of vader & flair sentiment scores"""
    # If no lyrics were found, return zeros.
    if lyrics == '!1':
        return (0,0)

    lines = cleanlyrics(lyrics)
    scores = []
    analyzers = {'flair':0, 'vader': 0}
    total_scores = {'flair':0, 'vader': 0}
    for line in lines:
        scores.append(
            (
                line, {
                    'flair': flair_sentiment(line),
                    'vader': vader_sentiment(line),
                }
            )
        )

        total_scores['flair'] += scores[-1][1]['flair']
        total_scores['vader'] += scores[-1][1]['vader']
        
    # Return normalized results:
    return (
        total_scores['vader'] / len(lines),
        total_scores['flair'] / len(lines)
    )


def cleanlyrics(lyrics):
    """
    Returns the lines of input lyrics without any blanks,
    brackets, or accented characters.
    """
    # Remove brackets (), and remove all content in [] brackets
    lyrics = lyrics.replace('(','').replace(')','')
    lyrics = re.sub("[\[].*?[\]]", "", lyrics)

    # unaccent string:
    lyrics = unidecode.unidecode(lyrics)
    
    # Remove blank lines
    blanklines = True
    while blanklines:
        lyrics = lyrics.replace('\n\n','\n')
        if '\n\n' not in lyrics:
            blanklines = False
    
    # Split lines and remove blanks / single character lines:
    return [line for line in lyrics.split('\n') if len(line) > 1]


def flair_sentiment(phrase):
    sentence = Sentence(phrase)

    # call predict
    FLAIR.predict(sentence)
    
    score = 0
    if sentence.tag == 'NEGATIVE':
        score = sentence.score * -1
    elif sentence.tag == 'POSITIVE':
        score = sentence.score

    return score

def vader_sentiment(phrase):
    return VADER.polarity_scores(phrase)['compound']
