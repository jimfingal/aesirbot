from unipath import Path
import re
import io
import langid
from bs4 import BeautifulSoup
import json
import nltk
import botutils
import logging

# I managed to do practice TDD with this up until this function.
def get_sentences_from_relevant_songs(data_path):

    aesir_words = get_aesir_words()
    logging.info("Looking for words overlapping with: %s" % aesir_words)

    for song_text in get_english_song_texts(data_path):

        cleaned_sentences = split_and_clean(song_text)
        joined = "\n".join(cleaned_sentences)
        word_tokenized = nltk.tokenize.word_tokenize(unicode(joined.lower(), errors='replace'))

        if overlap_words(word_tokenized, aesir_words):
            for sentence in cleaned_sentences:
                if is_english_text(sentence):
                    yield sentence


def get_english_song_texts(data_path):
    for song in read_songs(data_path):
        song_text = get_text_from_song_html(song)
        if is_english_text(song_text):
            yield song_text

def read_songs(data_path):
    for album_text in read_albums(data_path):
        songs = split_songs(album_text)
        for song in songs:
            yield song

def read_albums(data_path):
    for album_path in walk_path(data_path):
        album_text = get_file_text(album_path)
        yield album_text

def walk_path(path):
    for album_file in path.walk(filter=lambda p: p.isfile() and re.match(r".*html", p.name)):
        yield album_file

def get_file_text(path):
    with io.open(path.absolute(), 'r', encoding='utf-8') as f: 
        file_text = f.read().decode('utf-8')
        return file_text

def split_songs(text):
    songs = []
    for song in text.split('<h3>'):
        if "a name" in song:
            songs.append("<h3>" + song)
    return songs

def is_english_text(text):
    language = langid.classify(text)
    return language[0] == "en"

def get_text_from_song_html(song):
    soup = BeautifulSoup(song)
    trash = [s.extract() for s in soup('h3')]
    trash = [s.extract() for s in soup('a')]
    trash = [s.extract() for s in soup('i')]
    trash = [s.extract() for s in soup.select('div')]

    song_text = soup.text.strip()
    return song_text

def split_and_clean(song_text):
    sentences = botutils.text.tokenize_sentences(song_text.strip())
    only_real_sentences = filter(lambda x: len(x) >= 15, sentences)
    cleaned = map(botutils.text.remove_space_before_punctuation, only_real_sentences)
    cleaned = map(botutils.text.collapse_multiple_whitespace, cleaned)
    cleaned = map(botutils.text.remove_trailing_punctuation, cleaned)
    cleaned = map(botutils.text.remove_leading_punctuation, cleaned)
    cleaned = map(lambda x: x.strip(), cleaned)
    return cleaned


def get_aesir_words():
    aesir_path = Path('./ebookofblackearth/aesir_words.json')
    word_list = json.loads(aesir_path.read_file())
    return set(word_list)

def overlap_words(corpus, words):
    '''Takes a list of tokenized words, and returns overlap with an enumerated set of test words'''
    return set(corpus).intersection(words)
