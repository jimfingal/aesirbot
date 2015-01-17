Ebook of Black Earth
=====

An Ebooks Twitter Bot that uses metal lyrics as the source corpus.

Most of the work to get this good was exploratory data analysis of the corpus. Turns out there are a lot of songs with Swedish lyrics, or misogynist crap that I don't want my bot tweeting.

# Scraping

To get the corpus for this, I crawled darklyrics using Scrapy. When I first tried to do this with default I got banned, so I backed off and used a Tor proxy. Setting up Tor manually / via command line proved frustrating, whereas using the OSX package was super easy: http://tor.hermetix.org/docs/tor-doc-osx.html.en

Scrapy run by going to darklyrics folder and running:

    scrapy crawl darkspider

This puts all of the data into a "data" directory


# Loading Data

The load_data.py script is run from the local machine, or wherever has the crawled HTML files, and populates Mongo with the corpus.

The Mongo documents are extremely simple -- the only reason I use Mongo here is that you can get more free storage on Heroku, which is useful for moderately-sized corpora; the biggest free Redis add-on only gives you 25 megs.

# Deploying

Uses buildpack for ease of numpy install:

    heroku config:set BUILDPACK_URL=https://github.com/thenovices/heroku-buildpack-scipy
