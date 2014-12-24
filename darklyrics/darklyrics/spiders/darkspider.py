
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from unipath import Path
import lxml.html


class DarkSpider(CrawlSpider):
    name = "darkpider"
    allowed_domains = ["www.darklyrics.com"]
    start_urls = (
        'http://www.darklyrics.com/a/abaddonincarnate.html',
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
        lyrics = lxml_body.cssselect(".lyrics")
        output = lxml.html.tostring(lyrics)

        if output:
            Path("../data/" + letter + "/").mkdir(parents=True)
            p = Path("../data/" + letter + "/" + filename)
            p.write_file(response.body)