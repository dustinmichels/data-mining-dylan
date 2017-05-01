import requests
from bs4 import BeautifulSoup
import re
import os
import pickle
from song import Song

SONGS = []  # a list of song objects


def get_all_songs():
    page = requests.get("https://bobdylan.com/songs/")
    soup = BeautifulSoup(page.content, 'html.parser')

    song_list = soup.find_all(class_='song')

    del song_list[0]    # not a song

    for song in song_list:
        song_url = song.find('a').attrs['href']
        get_song_data(song_url)


def get_song_data(song_url):
    page = requests.get(song_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    song_title = get_data_helper(soup, 'headline')
    song_author = get_data_helper(soup, 'credit')
    song_lyrics = get_data_helper(soup, 'lyrics')
    song_year = get_data_helper(soup, 'copytext')

    # Clean it up
    song_author, song_lyrics, song_year = cleanup_song_data(song_author, song_lyrics, song_year)

    #  Make song object, add to global list called SONGS
    song_id = str(len(SONGS))
    new_song = Song(song_id, song_title, song_author, song_lyrics, song_year)
    SONGS.append(new_song)

    # Write to text file
    write_to_file(new_song)

    print("Done: {}".format(song_title))
    return new_song


def get_data_helper(soup, class_name):
    try:
        return_text = soup.find_all(class_=class_name)[0].get_text()
    except IndexError:
        return_text = ""
    return return_text


def cleanup_song_data(song_author, song_lyrics, song_year):

    # Cleanup author text
    start_index = song_author.find("Written by: ")
    if start_index > -1:
        start_index += len("Written by: ")
        song_author = song_author[start_index:]
    song_author = song_author.replace("\t\t\t\t\t\t\t\t\t\t", "")  # usually at end

    # Cleanup lyrics text
    song_lyrics = song_lyrics.replace("\t\t\t", "")  # usually at start
    song_lyrics = song_lyrics.replace("\t\t\t\t\t\t\t\t\t\t", "")  # usually at end
    stop_index = song_lyrics.find("Copyright")
    if stop_index > -1:
        song_lyrics = song_lyrics[:stop_index]

    # Cleanup year text
    try:
        song_year = re.findall("\d+", song_year)[0]
    except IndexError:
        song_year = ""

    return song_author, song_lyrics, song_year


def write_to_file(write_song):

    filename = "songs/song_{}.txt".format(write_song.id)

    f = open(os.path.expanduser(filename), 'w', encoding='utf-8')

    f.write("--TITLE--\n")
    f.write(write_song.title)
    f.write("\n\n--AUTHOR--\n")
    f.write(write_song.author)
    f.write("\n\n--LYRICS--\n")
    f.write(write_song.lyrics)
    f.write("\n\n--YEAR--\n")
    f.write(write_song.year)
    f.write("\n\n--END--\n")

    f.close()


if __name__ == "__main__":
    get_all_songs()
    pickle.dump(SONGS, open('songs.p', 'wb'))
