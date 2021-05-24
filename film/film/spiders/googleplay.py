import pymongo
import scrapy
import json
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
import re


def first(x):
    if len(x) == 0:
        return ''
    else:
        return x[0]





class GooglePlaySpider(scrapy.Spider):
    name = 'googleplay'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.googleplay
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['google.com', 'justwatch.com']
        query = 'https://apis.justwatch.com/content/titles/en_PH/popular?body={"fields":["full_path"],"genres":["%s"],"providers":["ply"],"enable_provider_filter":false,"monetization_types":[],"page":1,"page_size":3,"matching_offers_only":true}&language=en'
        genres = ['act', 'ani', 'cmy', 'crm', 'doc', 'drm', 'eur', 'fml', 'fnt', 'hrr', 'hst', 'msc', 'rly', 'rma',
                  'scf', 'spt', 'trl', 'war', 'wsn']
        self.start_urls = [query % i for i in genres]

    # download_delay = 1.5 
    def parse(self, response):
        if self.state == 'run':
            data = json.loads(response.body)
            for item in data.get('items', []):
                yield Request('https://www.justwatch.com%s' % item.get('full_path'), callback=self.parse_justwatch)
            if data['page'] < data['total_pages']:
                yield Request(
                    response.url.replace('%22page%22:' + str(data['page']), '%22page%22:' + str(data['page'] + 1)))

    def parse_justwatch(self, response):
        url = response.xpath('//*[@alt="Google Play Movies"]/../@href').extract()[0]
        yield Request(url, callback=self.parse_googleplay)

    def parse_googleplay(self, response):
        is_duplicated = (len(list(self.collection.find({'url': response.url}, {'_id': 1}))) > 0)
        if is_duplicated:
            if self.crawl_type == 'incremental':
                self.state = 'stop'
            return
        yield {
            'title': first(response.xpath('//h1//text()').extract()),
            'url': response.url,
            'release_year': first(response.xpath('//h1/../div/div/div/span[1]/text()').extract()),
            'duration': first(response.xpath('//h1/../div/div/div/span[2]//text()').extract()),
            'genre': first(response.xpath('//a[@itemprop="genre"]/text()').extract()),
            'description': first(response.xpath('//span[@jsslot]/text()').extract()),
            'cast': response.xpath('//h2[text()="Actors"]/../div/span/a/span/text()').extract(),
            'producer': response.xpath('//h2[text()="Producers"]/../div/span/a/span/text()').extract(),
            'director': response.xpath('//h2[text()="Director"]/../div/span/a/span/text()').extract(),
            'writer': response.xpath('//h2[text()="Writers"]/../div/span/a/span/text()').extract()
        }
