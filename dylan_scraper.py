import json
import requests
import re
from bs4 import BeautifulSoup


def get_song_urls():
    """Returns list of URLs to every song"""
    page = requests.get("https://bobdylan.com/songs/")
    soup = BeautifulSoup(page.content, 'html.parser')
    return ([
        s.a['href']
        for s in soup.find_all(class_='song')[1:]])


def get_album_urls():
    """Returns list of URLs to every album"""
    page = requests.get('https://bobdylan.com/albums/')
    soup = BeautifulSoup(page.content, 'html.parser')
    return ([
        x.a['href']
        for x in soup.find_all('h3')])


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


if __name__ == "__main__":
    song_urls = get_song_urls()
    songs = [get_song_data(url) for url in song_urls]

    with open('data/songs.json', 'w') as f:
        json.dump(songs, f)
