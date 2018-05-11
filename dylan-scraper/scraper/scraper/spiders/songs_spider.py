import scrapy

NOT_LYRICS = ("Click the 'VIEW ALL' link at the right to see a list of"
                "Bob Dylan's live performances of this song.")

class SongsSpider(scrapy.Spider):
    name = "songs"

    start_urls = ['http://bobdylan.com/songs/']

    def parse(self, response):
        for href in response.css('span.song a::attr(href)').extract():
            yield response.follow(href, self.parse_song)

    def parse_song(self, response):
        # title
        title = response.css('h2.headline::text').extract_first()

        # author
        _auth = response.css('div.credit::text').extract_first()
        try:
            author = _auth.strip().split('by: ')[1]
        except:
            author = None

        # lyrics
        lyrics = response.css('div.lyrics::text').extract()
        lyrics = ''.join(lyrics).strip() if lyrics else ''
        lyrics = lyrics.replace(NOT_LYRICS, '')

        # first recording
        first = response.css('div.item.album small::text').extract_first()
        first = first.strip() if first else None

        # list of albums
        _alb = response.css('div.item.album.secondary small::text').extract()
        albums = [a.strip().split(' (')[0] for a in _alb] if _alb else []
        if first not in albums:
            albums.insert(0, first)

        # first played, last played, play count
        _play = response.css('div.played a::text').extract()
        first_played, last_played = _play if _play else (None, None)
        times_played = response.css('div.played .db::text').extract_first()

        return dict(
            title=title, author=author, lyrics=lyrics,
            albums=albums, first_recording=first,
            first_played=first_played, last_played=last_played,
            times_played=times_played)
