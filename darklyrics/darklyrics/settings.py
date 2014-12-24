# -*- coding: utf-8 -*-

# Scrapy settings for darklyrics project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'darkspider'

SPIDER_MODULES = ['darklyrics.spiders']
NEWSPIDER_MODULE = 'darklyrics.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'darklyrics (+http://www.yourdomain.com)'


COOKIES_ENABLED = False

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

DEPTH_LIMIT = 1