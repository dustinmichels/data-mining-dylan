import json
import requests
import re
from bs4 import BeautifulSoup


# ---------------- Songs ---------------- #
def get_song_urls():
    """Returns list of URLs to every song"""
    page = requests.get("https://bobdylan.com/songs/")
    soup = BeautifulSoup(page.content, 'html.parser')
    return ([
        s.a['href']
        for s in soup.find_all(class_='song')[1:]])


def safe_parse(func):
    """Catches parsing errors"""
    try:
        return func()
    except AttributeError:
        print("  Couldn't parse!")
        return ''


def get_song_data(song_url):
    """Returns dictionary of given song"""

    page = requests.get(song_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    not_lyrics = ("Click the 'VIEW ALL' link at the right to see a list "
                  "of Bob Dylan's live performances of this song.")

    # Title
    title = safe_parse(
        lambda: (soup.find(class_='headline')
                 .get_text(strip=True)))

    # Author
    author = safe_parse(
        lambda: (soup.find(class_='credit')
                 .get_text(strip=True)
                 .replace('Written by: ', '')))

    # Lyrics
    lyrics = safe_parse(
        lambda: (soup.find(class_='lyrics')
            .get_text()
            .replace('\t', '').strip()
            .replace(not_lyrics, '')
            .split('Copyright ©')[0]))

    # Albums
    albums = list(set(safe_parse(
        lambda: ([
            re.sub(r'\([^)]*\)', '', album.get_text()).strip()
            for album
            in soup.find_all('small')]))))

    print("Done: {}".format(title))

    return dict(
        title=title, author=author, lyrics=lyrics,
        albums=albums, url=song_url)


# ---------------- Albums ---------------- #
def get_album_urls():
    """Returns list of URLs to every album"""
    page = requests.get('https://bobdylan.com/albums/')
    soup = BeautifulSoup(page.content, 'html.parser')
    return ([
        x.a['href']
        for x in soup.find_all('h3')])


def get_album_data(album_url):
    page = requests.get(album_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    cover_url = soup.find(class_='cover').find('img')['src']
    headline = (soup.find(class_='headline').get_text(strip=True))
    title = headline[:headline.find('(')].strip()
    year = headline[headline.find("(") + 1:headline.find(")")]

    track_list = [
        x.get_text(strip='true').split('. ')[1]
        for x in soup.find_all(class_='track')]

    return dict(
        title=title, year=year, cover_url=cover_url,
        track_list=track_list, url=album_url)


# ---------------- Shows ---------------- #
def _get_filtered_tour_urls():
    page = requests.get('https://www.bobdylan.com/setlists')
    soup = BeautifulSoup(page.content, 'html.parser')
    return [
        x['href']
        for x in soup.find(class_='buy-options').find_all('a')]


def _get_setlist_urls(filter_url):
    page = requests.get(filter_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tour_urls = soup.find(class_='tour-list').find_all('a', {'class', 'date'})
    return [x['href'] for x in tour_urls]


def get_all_setlist_urls():
    all_setlist_urls = []
    filter_urls = _get_filtered_tour_urls()
    for url in filter_urls:
        all_setlist_urls.extend(_get_setlist_urls(url))
    return all_setlist_urls


def get_show_data(setlist_url):
    page = requests.get(setlist_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    date = safe_parse(lambda: soup.find(class_='date').get_text())
    place = safe_parse(lambda: soup.find(class_='headline').get_text())
    venue = safe_parse(lambda: soup.find(class_='venue').get_text())
    _setlist = safe_parse(lambda: soup.find(class_='set-list').find_all(class_='title'))
    setlist = [x.get_text() for x in _setlist]

    return dict(date=date, place=place, venue=venue, setlist=setlist)


if __name__ == "__main__":

    song_urls = get_song_urls()
    album_urls = get_album_urls()
    setlist_urls = get_all_setlist_urls()

    song_data = [get_song_data(url) for url in song_urls]
    album_data = [get_album_data(url) for url in album_urls]
    show_data = [get_show_data(url) for url in setlist_urls]

    with open('data/songs.json', 'w') as f:
        json.dump(song_data, f)
    with open('data/albums.json', 'w') as f:
        json.dump(album_data, f)
    with open('data/shows.json', 'w') as f:
        json.dump(show_data, f)
