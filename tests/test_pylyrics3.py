'''Tests for PyLyrics3'''
import unittest
import pylyrics3


class TestPyLyrics3(unittest.TestCase):
    '''Test class for PyLyrics3'''

    # TODO: Write more obscure test cases (eg, all special handled chars?)

    def test_get_song_lyrics(self):
        '''PyLyrics3 can get a song given artist and title'''
        twenty2 = pylyrics3.get_song_lyrics('bon iver', '22 (OVER S∞∞N)')
        self.assertTrue('might be over soon' in twenty2)

    def test_album(self):
        '''PyLyrics3 parses albums with tracks'''
        bon_iver = pylyrics3.get_artist_lyrics('bon iver', albums=True)
        self.assertTrue('22, a Million (2016)' in bon_iver)
        self.assertTrue(len(bon_iver['22, a Million (2016)']) > 2)

    def test_emo(self):
        '''PyLyrics3 can handle special characters'''
        fame = pylyrics3.get_song_lyrics('fall out boy', 'fame < infamy')
        self.assertTrue('preacher' in fame)

    def test_get_artist(self):
        '''PyLyrics3 can grab all tracks by an artist'''
        l = pylyrics3.get_artist_lyrics('lorde')
        self.assertTrue('Tennis Court' in l)
        self.assertTrue('you think that' in l['Tennis Court'])


if __name__ == '__main__':
    unittest.main()
