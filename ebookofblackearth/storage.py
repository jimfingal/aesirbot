from mongoengine import Document, StringField
import logging
import mongoengine
import botutils

class CorpusText(Document):
    text = StringField(required=True)

def connect_mongo(app):
    mongo_uri = botutils.config.get_mongo_uri(app)
    if mongo_uri:
        db = mongo_uri.split('/')[-1]
        logging.info("Connecting to host, db %s" % db)
        mongoengine.connect(db, host=mongo_uri)
    else:
        logging.info("Connecting mongo to default")
        mongoengine.connect(app)
