# pylyrics3
Lyric scraper very loosely based on py-lyrics, updated for Python 3

# Installation
Install with `pip install pylyrics3`

# Usage
`pylyrics3` has 3 main functions:
 - `get_artist_lyrics(artist, albums=False)` - scrapes and returns all lyrics by a particular artist as a dict keyed by song title. If `albums=True`, will return a nested dict keyed by album title and then song title (see below).
 - `get_song_lyrics(artist, song)` - scrapes and returns the lyrics of a song as a string
 - `get_lyrics_from_url(url)` - scrapes the lyrics off the specified lyric wiki url  

```
>>> import pylyrics3

>>> bon_iver_lyrics = pylyrics3.get_artist_lyrics('bon iver')

>>> bon_iver_lyrics.keys()
dict_keys(['Come Talk To Me', 'Towers', 'Woods', ...)
>>> bon_iver_lyrics['Skinny Love']
"Come on skinny love, just last the year ..."

>>> bon_iver_albums = pylyrics3.get_artist_lyrics('bon iver', albums=True)
>>> bon_iver_albums.keys()
dict_keys(['For Emma, Forever Ago (2007)', 'Blood Bank (2009)', 'Bon Iver, Bon Iver (2011)', '22, a Million (2016)'])
>>> bon_iver_albums['22, a Million (2016)'].keys()
dict_keys(['22 (Over S∞∞N)', '10 D E A T H B R E A S T ⚄ ⚄', ...])
>>> bon_iver_albums['22, a Million (2016)']['22 (Over S∞∞N)']
"(It might be over soon, soon, soon) ..."

>>> pylyrics3.get_song_lyrics('drake', 'hotline bling')
"You used to call me on my, you used to, you used to ..."

>>> pylyrics3.get_lyrics_from_url('http://lyrics.wikia.com/wiki/Lorde:Tennis_Court')
"Don't you think that it's boring how people talk? ..."
```

You can also create a PyLyrics3 object and (optionally) pass it your own proxies like so:
```
>>> from pylyrics3 import PyLyrics3
>>> proxies = {...}
>>> pl3 = PyLyrics3(proxies=proxies)
>>> pl3.get_song_lyrics('drake', 'hotline bling')
"You used to call me on my, you used to, you used to ..."
```