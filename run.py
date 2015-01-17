import redis 
import logging

from botutils import config, twitter
from ebookofblackearth import aesirbot, storage

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)

APP_NAME = "AESIRBOT"

if __name__ == "__main__":

    config.check_config(APP_NAME)

    storage.connect_mongo(APP_NAME)
    redis_client = redis.from_url(config.get_redis_url(APP_NAME))

    markov = aesirbot.get_markov()
    
    tweet = aesirbot.get_tweet(markov, redis_client)
    logging.info(tweet)

    auth = twitter.get_auth(APP_NAME)
    tweepy = twitter.get_api(auth)

    tweepy.update_status(tweet)
