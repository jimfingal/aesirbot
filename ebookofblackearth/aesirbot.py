# -*- coding: utf-8 -*-

from botutils import ai
from storage import CorpusText
import md5
import logging
import langid
from songparser import get_aesir_words, overlap_words
import nltk
import re

REDIS_COLLECTION = 'posted'
AESIR_WORDS = get_aesir_words()


def get_markov(n=3):

    markov = ai.MarkovChain(ngram_size=n)

    logging.info("Training markov chain")
    count = 0
    for corpus_sentence in CorpusText.objects():
        markov.train_sentence(corpus_sentence.text.encode('utf-8'))
        count += 1
        if count % 100 == 0:
            logging.debug("Trained %s sentences" % count)

    return markov

def get_tweet(markov, redis_client):

    for x in xrange(0, 10000):

        sentence = markov.generate_sentence()

        text_hash = get_text_hash(sentence)

        if already_generated_sentence(text_hash, redis_client) or \
            not contains_aesir_words(sentence) or \
            langid.classify(sentence)[0] != 'en':

            continue

        tweet = clean_tweet(sentence)
        
        if len(tweet) > 140:
            continue
        else:
            # TODO: refactor out in case posting tweet fails
            redis_client.sadd(REDIS_COLLECTION, text_hash)
            return tweet

    return None


def get_text_hash(text):
    m = md5.new()
    m.update(text.lower())
    return m.hexdigest()

def already_generated_sentence(text_hash, redis_client):
    return redis_client.sismember(REDIS_COLLECTION, text_hash)

def contains_aesir_words(sentence):
    word_tokenized = nltk.tokenize.word_tokenize(unicode(sentence, errors='replace'))
    overlap = overlap_words(word_tokenized, AESIR_WORDS)
    return overlap

def clean_tweet(s):
    s = s.decode('utf-8')
    s = re.sub(r'\W+$','',s)
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace('`', '')
    s = s.replace('- ', '—')
    for word in AESIR_WORDS:
        s = s.replace(word, word.capitalize())
    s = s.replace(" i ", " I ")
    s = s.replace(" i,", " I,")
    s = s.replace("do n't", "don't")
    s = s + "!"
    return s
