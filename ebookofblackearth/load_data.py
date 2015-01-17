from unipath import Path
from storage import connect_mongo, CorpusText
from songparser import get_sentences_from_relevant_songs
from gevent import monkey
monkey.patch_all()

from bson.errors import InvalidStringData
import logging

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)

# TODO -- centralize
APP_NAME = "AESIRBOT"

if __name__ == "__main__":

    connect_mongo(APP_NAME)

    logging.info("Deleting existing sentences")
    CorpusText.objects().delete()
    
    logging.info("Processing sentences")

    seen_sentences = set()
    count = 0

    data_path = Path('./data')
    for sentence in get_sentences_from_relevant_songs(data_path):

        if sentence not in seen_sentences:
            seen_sentences.add(sentence)
     
            try:
                text = CorpusText(text=sentence)
                text.save()
            except InvalidStringData as e:
                logging.error(e)

            count += 1
            if count % 10 == 0:
                logging.info("Processed %s sentences" % count)