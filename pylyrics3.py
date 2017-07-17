'''
Loosely based on http://github.com/tremby/py-lyrics - thanks!
'''
import urllib.parse
import requests
from bs4 import BeautifulSoup


class PyLyrics3(object):
    '''
    Lyric-scraper object.
    '''
    __lyric_wiki_url = 'http://lyrics.wikia.com'

    def __init__(self, proxies=None):
        '''
        Params:
            Optional:
            proxies: dict - proxies for the object's _session property to use
        '''

        self._session = requests.Session()
        self._session.headers.update({'User-Agent': 'lyrics'})
        self._session.proxies = proxies

    def get_artist_lyrics(self, artist, albums=False):
        '''
        Params:
            artist: str - name of the artist whose lyrics will be scraped
            artist: boolean - flag to structure result dict by album. Default is
                False, setting to True will return a dict nested by album
        Returns dict with structure {song: lyrics}: {str: str}
        '''
        url = self._construct_lyricwiki_url(artist)
        try:
            soup = self.__get_soup(url)
        except ValueError:
            print("Sorry, we couldn't find a Wiki for '%s' on LyricWiki."
                  % artist)
            return
        if albums:
            return self.__parse_albums(self.__get_artist_album_links(soup))

        song_urls = self.__get_artist_song_links(soup)
        title_to_lyrics = {}
        for url in song_urls:
            title = self.__parse_song_title(url)
            lyrics = self.get_lyrics_from_url(url)
            if lyrics:
                title_to_lyrics[title] = lyrics
        return title_to_lyrics

    def get_song_lyrics(self, artist, title):
        '''
        Params:
            artist: str - name of artist
            title: str - name of song
        Returns str of scraped lyrics
        '''
        return self.get_lyrics_from_url(self._construct_lyricwiki_url(artist,
                                                                      title))

    def get_lyrics_from_url(self, url):
        '''Get and return the lyrics for the given song.
        Returns False if there are no lyrics (it's instrumental).
        TODO:
        Raises an IOError if the lyrics couldn't be found.
        Raises an IndexError if there is no lyrics tag.
        '''
        try:
            soup = self.__get_soup(url)
        except ValueError:
            page_name = self._decode_lyricwiki(url.split('/')[-1])
            artist = page_name.split(':')[0]
            title = page_name.split(':')[1]
            print("Ran into an error getting lyrics for ' % s' by %s!"
                  % (title, artist))
            return

        try:
            lyricbox = soup.select('.lyricbox')[0]
            # remove script tags
            [s.extract() for s in lyricbox.find_all('script')]
        except IndexError:
            return None
        # look for a sign that it's instrumental
        if len(soup.select('.lyricbox a[title=\'Instrumental\']')):
            return False
        # prepare output
        lyrics = []
        if lyricbox.text is not None:
            for string in lyricbox.stripped_strings:
                lyrics.append(string + ' \n ')
        return ''.join(lyrics).strip()

    def __parse_albums(self, albums):
        '''Given a collection of album <a> tags, fetch their lyrics
        Params:
            albums: collection - collection of <a> tags, each being a link to
                an album
        Returns:
            Dict with structure {album: {track: lyrics}}: {str: {str: str}}
        '''
        artist_dict = {}
        for album in albums:
            title = album.text
            tracks = self.__parse_multi_disc(self.__get_parent_h2(album))
            urls = [self.__lyric_wiki_url + a.get('href') for a in tracks]
            artist_dict[title] = {self.__parse_song_title(url):
                                  self.get_lyrics_from_url(url) for url in urls}
        return artist_dict

    # Lyric Wiki helper methods

    @staticmethod
    def _decode_lyricwiki(str_):
        '''Decode Lyric Wiki encoded str'''
        str_ = str_.replace('Less_Than', '<')
        str_ = str_.replace('Greater_Than', '>')
        str_ = str_.replace('Number_', '#')
        str_ = str_.replace('Sharp_', '#')
        str_ = str_.replace('%27', "'")
        str_ = str_.replace('_', ' ')
        return urllib.parse.unquote(str_)

    @staticmethod
    def _encode_lyricwiki(str_):
        '''Return a string in LyricWiki encoding.
        Substitutions are performed as described at
        < http: // lyrics.wikia.com / LyricWiki: Page_Names > .
        '''

        words = str_.split()
        newwords = []
        for word in words:
            newwords.append(word[0].capitalize() + word[1:])
        str_ = '_'.join(newwords)
        str_ = str_.replace('<', 'Less_Than')
        str_ = str_.replace('>', 'Greater_Than')

        # TODO: Support Sharp_ as a valid substitution for '#'.
        str_ = str_.replace('#', 'Number_')
        str_ = str_.replace('[', '(')
        str_ = str_.replace(']', ')')
        str_ = str_.replace('{', '(')
        str_ = str_.replace('}', ')')
        return str_

    @staticmethod
    def _construct_lyricwiki_url(artist, song_title=None, edit=False):
        '''Constructs a LyricWiki URL for an artist or song
        Params:
            artist: str - artist to link to
            Optional:
            song_title: str - specific song to link to
            edit: boolean - flag to get link to edit entry
        Returns str url'''
        base = PyLyrics3.__lyric_wiki_url + '/wiki/'
        page_name = PyLyrics3._encode_lyricwiki(artist)
        if song_title:
            page_name += ':%s' % PyLyrics3._encode_lyricwiki(song_title)

        if edit:
            return base + 'index.php?title=%s&action=edit' % page_name
        return base + page_name

    # Class helper methods

    @staticmethod
    def __parse_multi_disc(h2_tag):
        '''Given an album's h2 tag, find all <a> tags for tracks associated with
        the album
        Params:
            h2_tag: BeautifulSoup - h2 tag of album
        Returns list of <a> tags for tracks'''
        tracks = []
        soup = h2_tag.next_sibling
        while soup and soup.name != 'h2':
            if soup.name == 'ol':
                tracks += soup.select('li a')
            soup = soup.next_sibling
        return tracks

    @staticmethod
    def __get_artist_song_links(artist_soup):
        '''Given the soup of an artist page, get <a> tags of all tracks'''
        songs = []
        for link_tag in artist_soup.select('ol li a'):
            link = PyLyrics3.__lyric_wiki_url + link_tag.get('href')
            songs.append(link)
        return songs

    @staticmethod
    def __get_artist_album_links(artist_soup):
        '''Given the soup of an artist page, get <a> tags of all albums'''
        return artist_soup.select('h2 .mw-headline a')

    @staticmethod
    def __get_parent_h2(album_a_tag):
        '''Given the soup of an album's <a> tag, get its h2 parent'''
        return album_a_tag.parent.parent

    @staticmethod
    def __parse_song_title(url):
        '''Given a LyricWiki encoded url, parse out the song title'''
        return PyLyrics3._decode_lyricwiki(url.split(':')[2])

    # IO Helper methods

    def __get_soup(self, url):
        '''Download and parse a URL as a BeautifulSoup object'''
        req = self._session.get(url)
        try:
            self.__check_response(req.status_code)
            # lxml is much speedier than the normal parser, but requires install
            try:
                return BeautifulSoup(req.text, 'lxml')
            except ValueError:
                return BeautifulSoup(req.text, 'html.parser')
        except AssertionError:
            print('Unable to download url ' + url)
            raise ValueError('Status', req.status_code)

    @staticmethod
    def __check_response(status_code):
        '''Raises an assertion error if the status code is not a success'''
        first_digit = status_code // 100
        assert first_digit in (2, 3)


# support for importing just the functions
__INSTANCE = PyLyrics3()

get_song_lyrics = __INSTANCE.get_song_lyrics
get_artist_lyrics = __INSTANCE.get_artist_lyrics
get_lyrics_from_url = __INSTANCE.get_lyrics_from_url
