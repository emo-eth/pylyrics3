import requests
from bs4 import BeautifulSoup

"""
Based on http://github.com/tremby/py-lyrics
"""

JWSOUP_SESSION = requests.Session()  # use a session for persistence
user_agent = 'lyrics'
JWSOUP_SESSION.headers.update({'User-Agent': user_agent})


def _lyricwikicase(s):
    """Return a string in LyricWiki case.
    Substitutions are performed as described at
    <http://lyrics.wikia.com/LyricWiki:Page_Names>.
    Essentially that means capitalizing every word and substituting certain
    characters."""

    words = s.split()
    newwords = []
    for word in words:
        newwords.append(word[0].capitalize() + word[1:])
    s = "_".join(newwords)
    s = s.replace("<", "Less_Than")
    s = s.replace(">", "Greater_Than")
    # FIXME: "Sharp" is also an allowed substitution
    s = s.replace("#", "Number_")
    s = s.replace("[", "(")
    s = s.replace("]", ")")
    s = s.replace("{", "(")
    s = s.replace("}", ")")
    # s = urllib.parse.urlencode([(0, s)])[2:]
    return s


def _lyricwikipagename(artist, title):
    """Return the page name for a set of lyrics given the artist and
    title"""

    return "%s:%s" % (_lyricwikicase(artist), _lyricwikicase(title))


def _lyricwikiurl(artist, title, edit=False):
    """Return the URL of a LyricWiki page for the given song, or its edit
    page"""

    base = "http://lyrics.wikia.com/wiki/"
    pagename = _lyricwikipagename(artist, title)
    if edit:
        return base + "index.php?title=%s&action=edit" % pagename
    return base + pagename


def get_lyrics(artist, title):
    """Get and return the lyrics for the given song.
    Raises an IOError if the lyrics couldn't be found.
    Raises an IndexError if there is no lyrics tag.
    Returns False if there are no lyrics (it's instrumental)."""

    soup = _get_soup(
        _lyricwikiurl(artist, title), fail=True)

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


def _get_soup(url, headers=None, cookies=None, timeout=None, fail=True):
    req = JWSOUP_SESSION.get(
        url, headers=headers, cookies=cookies, timeout=timeout)
    try:
        _check_response(req.status_code)
        return BeautifulSoup(req.text, 'lxml')
    except AssertionError:
        print('Unable to download url ' + url)
        if fail:
            raise ValueError('Status', req.status_code)
        return BeautifulSoup('', 'lxml')


def _check_response(status_code):
    first_digit = status_code // 100
    assert first_digit in {2, 3}
