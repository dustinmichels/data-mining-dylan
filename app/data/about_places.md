We can see that New York and New Orleans wiggle there was into the most Dyaln songs (6 counts each). Most cities mentioned are in the United States, but places all across Europe and South America get mentioned too, as well as a few places in Asia and the Middle East.

## Data Aquisition

Lyrics and song metadata were scraped from BobDylan.com with Python, using Scrapy. See scraping code [here](https://github.com/dustinmichels/data-mining-dylan/blob/master/dylan-scraper/scraper/scraper/spiders/songs_spider.py).

## Counting Places

Place identification and counting also happened in Python. A Jupyter Notebook with code can be viewed [here](https://hub.mybinder.org/user/dustinmichels-data-mining-dylan-gaxjyab0/notebooks/notebooks/find_cities.ipynb).

Procedure:

1. For all song lyrics, capitalized n-grams of length 1 and 2 were extracted using the regex `re.findall('([A-Z][a-z]+)', text)`.
    - For instance, "Denver" is a 1-gram and "San Francisco" is a 2-gram that would be matched by the regex.
2. The found n-grams were cross-referenced against a list of cities, with metadata like lat/lon, population, to identify actual cities (vs. other capitalized words). If multiple cities had the same name, the one with greater population was used.
3. A few found cities were manually excluded. They are capitilized words in Dylan songs that correspond to real cities, but upon closer inspection, do not appear to the be places he's singing about. Ie, when Dylan says "Man" he's talking about Mankind, not the city in western Ivory Coast. Specifically, I excluded:
`['Man', 'San', 'Orleans', 'Mary', 'York', 'Young', 'Same',
'Ye', 'Darwin', 'Orange', 'George', 'Bo', 'Leo', 'Gay',
'Buy', 'Split', 'Nice', 'Nancy', 'Montana', 'Florida']`
4. Plces identified in lyrics were counted.
5. A data table of city names, counts, and songs they appear in, as well as metadata about the cities and songs was compiled.
6. The data was formatted as a [geojson](http://geojson.org/) file, and saved.

## Interactive Map

The places in the GeoJson file were mapped using [Leaflet.js](https://leafletjs.com/). That map was incorporated into the interactive, custom web app you see, built using HTML, CSS, and JavaScript (employing the [Vue.js](https://vuejs.org/) JavaScript framework).