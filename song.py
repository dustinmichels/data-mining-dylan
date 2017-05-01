class Song:
    """
    Used to store the Dylan songs we scrape.
    Fields: Unique id, title, author, lyrics, year recorded
    """
    def __init__(self, song_id, song_title, song_author, song_lyrics, song_year):
        self.id = song_id
        self.title = song_title
        self.author = song_author
        self.lyrics = song_lyrics
        self.year = song_year

    @property
    def __str__(self):
        return f'Song: {self.title}'

    @property
    def __repr__(self):
        return f'SONG: {self.title}, {self.author}'