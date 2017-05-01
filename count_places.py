import csv
import os
import pickle

import named_entities as ne
import get_context as gc
from song import Song


def main():
    song_list = load_pickle()   # list of Song objects
    city_count = {}             # dictionary where city_tuple is key, and value is dictionary of {count, songs, lyrics}

    for song in song_list:
        print("\n---------")
        print(song.title)
        city_count = update_city_count(song, city_count)

    write_to_csv(city_count)


def load_pickle() -> list:
    """
    :return: List of Song objects
    """
    full_song_list = pickle.load(open("songs.p", "rb"))
    return full_song_list


def update_city_count(song, city_count):

    cities_list = identify_cities(song.lyrics)  # Get list of city_tuples (city, lat, long) mentioned in the song
    context_dict = get_context(song.lyrics, cities_list)  # get contexts of use

    for city_tuple in cities_list:

        song_title = f'{song.title} ({song.year})'
        song_context = f'{song.title.upper()}: "...{context_dict[city_tuple]}"'

        if city_tuple not in city_count:
            city_count[city_tuple] = {
                'count': 1,
                'songs': [song_title],
                'context': [song_context]
            }
            print("adding new city_tuple to city_list...")
        elif city_tuple in city_count:
            city_count[city_tuple]['count'] += 1
            city_count[city_tuple]['songs'].append(song_title)
            city_count[city_tuple]['context'].append(song_context)
            print("updating count...")
    return city_count


def identify_cities(lyrics):
    cities = []

    # get potential cities from song, using named_entities
    potential_places = ne.get_named_entities(lyrics)
    print('potential places: {}'.format(potential_places))

    # open cities.csv, check set of potential places against known places
    with open('cities.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            if row[0] in potential_places:
                # Tuple containing city name (row[0]), lat (row[2]), and lon (row[3]).
                city = (row[0], row[2], row[3])
                # city = {"name": row[0], "lat": row[2], "lon": row[3]}
                cities.append(city)
                print(f"actual places: {cities}")

    return cities


def get_context(lyrics, cities_list):

    context_dict = {}

    for city_tuple in cities_list:
        context = gc.get_context(city_tuple[0], lyrics)
        context_dict[city_tuple] = context

    return context_dict


def write_to_csv(city_count):

    write_list = make_list_for_writing_csv(city_count)

    with open("counts.csv", 'w', newline='', encoding='utf-8-sig') as csv_file:
        fieldnames = ['city', 'lat', 'lon', 'count', 'songs', 'context']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for item in write_list:
            print(item)
            writer.writerow(item)

        print("success")


def make_list_for_writing_csv(city_count):
    write_list = []

    for k in city_count:
        new_entry = {
            'city': k[0],
            'lat': k[1],
            'lon': k[2],
            'count': city_count[k]['count'],
            'songs': ", ".join(city_count[k]['songs']),
            'context': '; '.join(city_count[k]['context'])
        }

        write_list.append(new_entry)

    return write_list


def get_lyrics_from_text_file(song_id):
    """
    Not used by main method.
    :param song_id: 
    :return: 
    """

    filename = "songs/song_{}.txt".format(song_id)

    with open(os.path.expanduser(filename), 'r') as f:
        sample = f.read()

    start_index = sample.find("--LYRICS--") + len("--LYRICS--")
    end_index = sample.find("--YEAR--")

    lyrics = sample[start_index:end_index]
    return lyrics

if __name__ == "__main__":
    main()
