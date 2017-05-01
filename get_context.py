"""
get_context.py
"""

import nltk


def get_context(city, lyrics):

    i = lyrics.find(city)

    start_index = i-30
    if start_index < 0:
        start_index = 0

    end_index = i+30
    if end_index > len(lyrics):
        end_index = len(lyrics)

    context = lyrics[start_index: end_index]

    tokenized_text = nltk.word_tokenize(context)
    result = " ".join(tokenized_text)

    return result

