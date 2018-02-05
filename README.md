# data-mining-dylan

Some code for scraping Dylan lyrics, and quantifying references to places.

# How it works #

The "scrape_lyrics.py" file scrapes lyrics from BobDylan.com, using Requests and
Beautiful Soup. It uses the Song class contained in "song.py." It writes the songs
it scrapes to text files and also to a pickled file, called "songs.p"

The "count_places" module opens up the pickled file, "songs.p" and reconstructs a
list of Song objects. It finds named entities using "named_entities.py" and then
checks if named entities are cities using "cities.csv". It counts references to places
and writes the results to "counts.csv." It also uses "get_context.py" to grab a section
of text surrounding the place refereces, and writes that to the CSV as well.

The map I made can be viewed at:
https://dustin7538.carto.com/viz/12a26da4-2df0-11e7-a569-0e3ff518bd15/public_map
