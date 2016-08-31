# pylyrics3
Lyric scraper very loosely based on py-lyrics, updated for Python 3

# Installation
Install with `pip install pylyrics3`

# Usage
`pylyrics3` has 3 main functions:
 - `get_artist_lyrics(artist)` - scrapes and returns all lyrics by a particular artist as a dict keyed by song title
 - `get_song_lyrics(artist, song)` - scrapes and returns the lyrics of a song as a string
 - `get_lyrics_from_url(url)` - scrapes the lyrics off the specified lyric wiki url  

```
>>> import pylyrics3

>>> bon_iver_lyrics = pylyrics3.get_artist_lyrics('bon iver')

>>> bon_iver_lyrics.keys()
dict_keys(['Come Talk To Me', 'Towers', 'Woods', ...)
>>> bon_iver_lyrics['Skinny Love']
"Come on skinny love, just last the year ..."

>>> pylyrics3.get_song_lyrics('drake', 'hotline bling')
"You used to call me on my, you used to, you used to ..."

>>> pylyrics3.get_lyrics_from_url('http://lyrics.wikia.com/wiki/Lorde:Tennis_Court')
"Don't you think that it's boring how people talk? ..."
```