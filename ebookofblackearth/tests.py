import unittest
import sure
import songparser as load_data

class TestLoadData(unittest.TestCase):

    def test_get_sentences_from_relevant_songs(self):
        sentence_gen = load_data.get_sentences_from_relevant_songs()
        sentence = sentence_gen.next()
        sentence.should_not.be.none
        len(sentence).should.be.greater_than(5)

    def test_path_exists(self):
        p = load_data.get_path()
        p.exists().should.be.true

    def test_walk_path(self):
        p = load_data.get_path()
        
        gen = load_data.walk_path(p)
        album = gen.next()

        album.should_not.be.none
        str(album).should.contain("aaaarrghh")

    def test_read_file(self):

        p = load_data.get_path()
        
        gen = load_data.walk_path(p)
        album = gen.next()

        text = load_data.get_file_text(album)
        text.should_not.be.none
        text.should.contain('<div class="lyrics">')


    def test_split_songs(self):

        song1 = "<h3><a name='1'>Some title</h3>Some Lyrics!"
        song2 = "<h3><a name='2>Some title</h3>Some Lyrics!"
        songs = song1 + song2

        songs = load_data.split_songs(songs)

        len(songs).should.equal(2)
        songs[0].should.equal(song1)
        songs[1].should.equal(song2)

    def test_english_text(self):

        load_data.is_english_text("This is an english text").should.be.true
        load_data.is_english_text("Sammasta kiipesin kannelle taivaan").should.be.false

    def test_get_songs(self):

        song_gen = load_data.read_songs(load_data.get_path())
        song = song_gen.next()
        song.should_not.be.none
        len(song).should.be.greater_than(100)

    def test_get_albums(self):
        album_gen = load_data.read_albums(load_data.get_path())
        album = album_gen.next()
        album.should_not.be.none
        len(album).should.be.greater_than(1000)

    def test_get_song_text(self):

        song_gen = load_data.get_english_song_texts(load_data.get_path())
        song = song_gen.next()
        song.should_not.be.none
        len(song).should_not.contain("<h3>")

    def test_get_aesir_words(self):

        words = load_data.get_aesir_words()
        words.should.contain("odin")
        words.should.contain("thor")