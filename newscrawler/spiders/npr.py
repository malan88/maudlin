import scrapy
from dateutil import parser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from newscrawler.items import NewscrawlerItem
from bs4 import BeautifulSoup as BS
import logging

CLASS = 'paragraphs-container'

class NPRSpider(CrawlSpider):
    name = 'npr'
    allowed_domains = ['text.npr.org']
    start_urls = ['https://text.npr.org']
    rules = [
        Rule(LinkExtractor(allow='.*'), follow=True, callback='parse')
    ]

    def parse(self, response):
        item = NewscrawlerItem()
        item['agency'] = self.name
        item['start'] = self.start_urls[0]
        item['url'] = response.url

        item['title'] = response.css('h1.story-title::text').get()
        item['byline'] = response.css('.story-head > p:nth-child(2)::text').get()

        date = response.css('.story-head > p:nth-child(3)::text').get()
        if not date:
            return None
        date = date.replace('• ', '')

        date = parser.parse(date)
        item['date'] = date

        soup = BS(response.text)
        container = soup.find('div', class_=CLASS)
        paragraphs = container.find_all('p', id=None)
        text = []
        for p in paragraphs:
            text.append(p.text.strip())
        item['text'] = '\n\n'.join(text)
        if len(item['text']) < 100:
            return None
        return item
