import redis 
import logging
import random

from botutils import config, twitter, ai
from ebookofblackearth import aesirbot, storage

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)


if __name__ == "__main__":

    APP_NAME = storage.APP_NAME

    ai.boostrap_nltk_data()

    config.check_config(APP_NAME)

    storage.connect_mongo(APP_NAME)
    redis_client = redis.from_url(config.get_redis_url(APP_NAME))

    n = random.choice([2, 3])
    logging.info("Using %s-grams" % n)
    markov = aesirbot.get_markov(n=n)
    
    tweet = aesirbot.get_tweet(markov, redis_client)
    logging.info(tweet)

    auth = twitter.get_auth(APP_NAME)
    tweepy = twitter.get_api(auth)

    tweepy.update_status(tweet)
