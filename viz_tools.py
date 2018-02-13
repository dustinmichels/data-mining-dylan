import ipywidgets as widgets
import folium


def get_place_selector(city_df, songs_df):
    """Return custom Jupyter widget"""

    # Reset index
    city_df = city_df.set_index('city')
    songs_df = songs_df.set_index('title')

    # Define some widgets
    sel = widgets.Dropdown(options=sorted(list(city_df.index.unique())))
    text = widgets.HTML(disabled=False)
    song_selector = widgets.Select(options=city_df.loc[sel.value, 'songs'])
    lyrics_viewer = widgets.HTML(placeholder='Lyrics...')

    # Piece together
    view = widgets.VBox([
        widgets.HBox([sel, text]),
        widgets.HBox([song_selector, lyrics_viewer])])

    def handle_city_change(change):
        count = city_df.loc[change.new, 'cnt']
        songs = city_df.loc[change.new, 'songs']
        text.value = '<b>Count:</b> {}</br>'.format(count)
        song_selector.options = songs
        song_selector.value = song_selector.options[0]

    def handle_song_change(change):
        city = sel.value
        lyrics = songs_df.loc[change.new, 'lyrics']
        lyrics = lyrics.replace('\n', '\\')
        idx = lyrics.find(city)
        lyric_text = '...' + lyrics[max(idx-50, 0):idx+100] + '...'
        lyric_text = lyric_text.replace(city, f'<b>{city}</b>')
        lyric_text = lyric_text.replace(city, f'<span style="color:blue">{city}</span>')
        lyrics_viewer.value = '<b>Lyrics:</b> {}</br>'.format(lyric_text)

    sel.observe(handle_city_change, names='value')
    song_selector.observe(handle_song_change, names='value')

    return view


def make_map(city_df):
    folium_map = folium.Map(location=(city_df.loc[0, 'lat'], city_df.loc[0, 'lng']), zoom_start=3)

    popup_text = ("{}<br>"
                  "Count: {}<br>")

    for idx, row in city_df.iterrows():
        folium.CircleMarker(
            location=(row.lat, row.lng),
            radius=row.cnt,
            color="green",
            fill=True,
            popup=folium.Popup(
                html=popup_text.format(row.city, row.cnt),
                max_width=1000)
        ).add_to(folium_map)

    return folium_map