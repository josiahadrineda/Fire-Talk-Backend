"""For use in ArticleScraper.py"""

from scrapyscript import Job, Processor
from scrapy.spiders import Spider
from scrapy import Request
import json

class PySpider(Spider):
    """Article scraping mechanism.
    """

    name = 'spi'
    n = 0

    def start_requests(self):
        yield Request(self.url)

    def parse(self, response):
        for sel in response.xpath("//div[@class='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc']")[:PySpider.n]:
            link = sel.xpath("a/@href").extract()
            yield {'link': f'https://news.google.com{link}'}

def scrape_articles(city, n):
    """Returns N articles regarding fires at or near CITY.
    """

    google_job = Job(PySpider, url=f'https://news.google.com/search?q={city} fire')

    PySpider.n = n

    processor = Processor(settings=None)

    data = processor.run(google_job)

    return json.loads(json.dumps(data))