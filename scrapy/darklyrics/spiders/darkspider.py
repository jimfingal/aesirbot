
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from unipath import Path
import lxml.html
from scrapy import log

class DarkSpider(CrawlSpider):
    name = "darkspider"
    allowed_domains = ["www.darklyrics.com"]
    start_urls = (
        'http://www.darklyrics.com/',
    )

    rules = (
        Rule(LinkExtractor(allow=('.*www.darklyrics.com/\w/\w+.html', ))),
        Rule(LinkExtractor(allow=('.*www.darklyrics.com/\w.html', ))),
        Rule(LinkExtractor(allow=".*www.darklyrics.com/lyrics/\w+/\w+.html.*"),
            callback='save_file',
            follow=True),
    )

    def save_file(self, response):

        split_url = response.url.split("/")
        album = split_url[-1].split('.')[0]
        artist = split_url[-2]
        letter = artist[0]

        filename = "%s_%s.html" % (artist, album)

        lxml_body = lxml.html.fromstring(response.body)
        lyrics = lxml_body.cssselect(".lyrics")[0]
        output = lxml.html.tostring(lyrics)

        if output:
            Path("../data/" + letter + "/").mkdir(parents=True)
            p = Path("../data/" + letter + "/" + filename)
            if not p.exists():
                log.msg("Writing: %s" % filename, level=log.INFO)
                #p.write_file(output)