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


class AppleITunesSpider(scrapy.Spider):
    name = 'appleitunes'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.appleitunes
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['apple.com', 'justwatch.com']
        query = 'https://apis.justwatch.com/content/titles/en_PH/popular?body={"fields":["full_path"],"genres":["%s"],"providers":["itu"],"enable_provider_filter":false,"monetization_types":[],"page":1,"page_size":3,"matching_offers_only":true}&language=en'
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
        url = response.xpath('//*[@alt="Apple iTunes"]/../@href').extract()[0]
        yield Request(url, callback=self.parse_appleitunes)

    def parse_appleitunes(self, response):
        is_duplicated = (len(list(self.collection.find({'url': response.url}, {'_id': 1}))) > 0)
        if is_duplicated:
            if self.crawl_type == 'incremental':
                self.state = 'stop'
            return
        yield {
            'title': first(response.xpath('//header/h1/text()').extract()).replace('\u202c', '').replace('\u202a', ''),
            'url': response.url,
            'release_year': first(response.xpath('//time/text()').extract()),
            'maturity_number': first(response.xpath('//h3/span[1]/text()').extract()),
            'duration': first(response.xpath('//header/ul[2]/li[1]/ul/li[2]/text()').extract()).strip(),
            'genre': response.xpath('//header/ul/li/ul/li/a/text()').extract(),
            'description': first(response.xpath('//header//p[@data-test-bidi]/text()').extract()),
            'cast': [x.strip() for x in
                     response.xpath('//span[text()="Cast"]/../../dd[@class="cast-list__detail"]/a/text()').extract()],
            'director': [x.strip() for x in response.xpath(
                '//span[text()="Director"]/../../dd[@class="cast-list__detail"]/a/text()').extract()],
            'producer': [x.strip() for x in response.xpath(
                '//span[text()="Producers"]/../../dd[@class="cast-list__detail"]/a/text()').extract()],
            'screenwriter': [x.strip() for x in response.xpath(
                '//span[text()="Screenwriter"]/../../dd[@class="cast-list__detail"]/a/text()').extract()],
            'studio': first(response.xpath('//dt[contains(text(),"Studio")]/../dd//text()').extract()).strip()
        }
