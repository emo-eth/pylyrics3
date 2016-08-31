import re
import urllib.parse
from bs4 import BeautifulSoup
import requests

"""
Loosely based on http://github.com/tremby/py-lyrics - thanks!
"""

# Use a requests session for persistence.
__SESSION = requests.Session()
__SESSION.headers.update({'User-Agent': 'lyrics'})


def get_artist_lyrics(artist):
    url = __construct_lyricwiki_url(artist)
    try:
        soup = __get_soup(url)
    except ValueError:
        print("Sorry, we couldn't find a Wiki for '%s' on LyricWiki." % artist)
        return
    song_urls = __get_artist_song_links(soup, artist)
    title_to_lyrics = {}
    for url in song_urls:
        title = __from_lyricwikicase(url.split(":")[2])
        lyrics = get_lyrics_from_url(url)
        if lyrics:
            title_to_lyrics[title] = lyrics
    return title_to_lyrics


def get_song_lyrics(artist, title):
    return get_lyrics_from_url(__construct_lyricwiki_url(artist, title))


def get_lyrics_from_url(url):
    """Get and return the lyrics for the given song.
    Returns False if there are no lyrics (it's instrumental).
    TODO:
    Raises an IOError if the lyrics couldn't be found.
    Raises an IndexError if there is no lyrics tag.
    """
    try:
        soup = __get_soup(url, fail=True)
    except ValueError:
        page_name = __from_lyricwikicase(url.split("/")[-1])
        artist = page_name.split(":")[0]
        title = page_name.split(":")[1]
        print("Ran into an error getting lyrics for '%s' by %s!"
              % (title, artist))
        return

    try:
        lyricbox = soup.select(".lyricbox")[0]
        # remove script tags
        [s.extract() for s in lyricbox('script')]
    except IndexError:
        return None
    # look for a sign that it's instrumental
    if len(soup.select(".lyricbox a[title=\"Instrumental\"]")):
        return False
    # prepare output
    lyrics = []
    if lyricbox.text is not None:
        for string in lyricbox.stripped_strings:
            lyrics.append(string + ' \n ')
    return "".join(lyrics).strip()


def __get_artist_song_links(soup, artist):
    song_regex = "^\/wiki\/%s:" % __lyricwikicase(artist)
    songs = []
    for elem in soup.find_all("li"):
        link_tag = elem.find("a", href=re.compile(song_regex))
        if link_tag:
            link = "http://lyrics.wikia.com" + link_tag.get("href")
            if "edit" not in link:
                songs.append(link)
    return songs


def __from_lyricwikicase(s):
    s = s.replace("Less_Than", "<")
    s = s.replace("Greater_Than", ">")
    s = s.replace("Number_", "#")
    s = s.replace("Sharp_", "#")
    s = s.replace("%27", "'")
    s = s.replace("_", " ")
    return urllib.parse.unquote(s)


def __lyricwikicase(s):
    """Return a string in LyricWiki case.
    Substitutions are performed as described at
    <http://lyrics.wikia.com/LyricWiki:Page_Names>.
    """

    words = s.split()
    newwords = []
    for word in words:
        newwords.append(word[0].capitalize() + word[1:])
    s = "_".join(newwords)
    s = s.replace("<", "Less_Than")
    s = s.replace(">", "Greater_Than")

    # TODO: Support Sharp_ as a valid substitution for "#".
    s = s.replace("#", "Number_")
    s = s.replace("[", "(")
    s = s.replace("]", ")")
    s = s.replace("{", "(")
    s = s.replace("}", ")")
    return s


def __construct_lyricwiki_url(artist, song_title=None, edit=False):
    """Constructs a LyricWiki URL for an artist or song.
    """
    base = "http://lyrics.wikia.com/wiki/"
    page_name = __lyricwikicase(artist)
    if song_title:
        page_name += ":%s" % __lyricwikicase(song_title)

    if edit:
        return base + "index.php?title=%s&action=edit" % page_name
    return base + page_name


def __get_soup(url, headers=None, cookies=None, timeout=None, fail=True):
    req = __SESSION.get(
        url, headers=headers, cookies=cookies, timeout=timeout)
    try:
        __check_response(req.status_code)
        return BeautifulSoup(req.text, 'lxml')
    except AssertionError:
        print('Unable to download url ' + url)
        if fail:
            raise ValueError('Status', req.status_code)
        return BeautifulSoup('', 'lxml')


def __check_response(status_code):
    first_digit = status_code // 100
    assert first_digit in {2, 3}
