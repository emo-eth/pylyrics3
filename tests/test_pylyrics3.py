import unittest
import pylyrics3


class TestPyLyrics3(unittest.TestCase):

    # TODO: Write more obscure test cases (eg, all special handled chars?)

    def test_get_song_lyrics(self):
        twenty2 = pylyrics3.get_song_lyrics('bon iver', '22 (OVER S∞∞N)')
        self.assertTrue('might be over soon' in twenty2)

    def test_emo(self):
        fame = pylyrics3.get_song_lyrics('fall out boy', 'fame < infamy')
        self.assertTrue('preacher' in fame)

    def test_get_artist(self):
        l = pylyrics3.get_artist_lyrics('lorde')
        self.assertTrue('Tennis Court' in l)
        self.assertTrue('you think that' in l['Tennis Court'])

if __name__ == '__main__':
    unittest.main()
