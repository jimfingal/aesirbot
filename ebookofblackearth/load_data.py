from unipath import Path
from storage import connect_mongo, CorpusText
from songparser import get_sentences_from_relevant_songs
from gevent import monkey
from bson.errors import InvalidStringData
import logging

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)

# TODO -- centralize
APP_NAME = "AESIRBOT"

if __name__ == "__main__":

    monkey.patch_all()
    connect_mongo(APP_NAME)
    
    data_path = Path('./data')

    logging.info("Deleting existing sentences")
    CorpusText.objects().delete()

    logging.info("Processing sentences")
    count = 0

    seen_sentences = set()
    for sentence in get_sentences_from_relevant_songs(data_path):

        if sentence not in seen_sentences:
            seen_sentences.add(sentence)
     
            try:
                text = CorpusText(text=sentence)
                text.save()
            except InvalidStringData as e:
                print e

            count += 1
            if count % 10 == 0:
                print "Processed %s sentences" % count