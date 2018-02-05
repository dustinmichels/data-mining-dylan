import pandas as pd
import spacy
from collections import Counter

df = pd.read_json('songs.json')
df.set_index('title', inplace=True)


def ner_cleanup(doc):
    doc.ents = [
        e for e in doc.ents
        if not(e.text.isspace() or
               e.text.endswith("’"))]
    return doc


def extract_places(text):
    print('.', end='')
    doc = nlp(text)
    return list(set([
        x.text.strip()
        for x
        in doc.ents
        if x.label_ == 'GPE']))


def count_places():

    c = Counter()

    nlp = spacy.load('en')
    nlp.add_pipe(ner_cleanup, after='ner')

    df['places'] = df.lyrics.apply(extract_places)

    for title, place_list in df.places.iteritems():
        c.update(place_list)
    return c


def get_place_counts():
    c = count_places()
    x = []
    y = []

    for k, v in c.most_common(10):
        x.append(k)
        y.append(v)

    return x, y
