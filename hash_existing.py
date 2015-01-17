from gevent import monkey
monkey.patch_all()

import logging

import redis 

from botutils import config, ai
from ebookofblackearth import aesirbot, storage

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)

# TODO -- centralize


if __name__ == "__main__":

    ai.boostrap_nltk_data()

    storage.connect_mongo(storage.APP_NAME)
    redis_client = redis.from_url(config.get_redis_url(storage.APP_NAME))

    for corpus_sentence in storage.CorpusText.objects():
        try:
            text_hash = aesirbot.get_text_hash(corpus_sentence.text)
            print corpus_sentence.text
            print text_hash
            redis_client.sadd(storage.REDIS_COLLECTION, text_hash)
        except UnicodeEncodeError as e:
            print e