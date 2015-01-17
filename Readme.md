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

TODO Include script that loads data into a db