# pylyrics3
Lyric scraper very loosely based on py-lyrics, updated for Python 3

# Installation
Point your terminal to the repo and type `python setup.py install` (if that doesn't work, try `sudo python setup.py install`) (replace `python` with whatever alias you have for Python 3!)

# Requirements
This module installs
- [Requests](http://docs.python-requests.org/en/master/user/install/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

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
"Come on skinny love, just last the year \n Pour a little salt, we were never here \n My, my, my, my, my, my, my, my ...""

>>> pylyrics3.get_song_lyrics('drake', 'hotline bling')
"You used to call me on my, you used to, you used to \n You used to call me on my cell phone \n Late night when you need my love ...""

>>> pylyrics3.get_lyrics_from_url('http://lyrics.wikia.com/wiki/Lorde:Tennis_Court')
""Don't you think that it's boring how people talk? \n Making smart with their words again, well, I'm bored ..."
```