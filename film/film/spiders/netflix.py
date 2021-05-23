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


def take_year(s):
    res = re.match(r'Release year: (\d+)', s)
    if res:
        return res.group(1)
    else:
        return "NA"


class NetflixSpider(scrapy.Spider):
    name = 'netflix'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.netflix
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['netflix.com', 'justwatch.com']
        query = 'https://apis.justwatch.com/content/titles/en_PH/popular?body={"fields":["full_path"],"genres":["%s"],"providers":["nfx"],"enable_provider_filter":false,"monetization_types":[],"page":1,"page_size":3,"matching_offers_only":true}&language=en'
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
        url = response.xpath('//*[@alt="Netflix"]/../@href').extract()[0]
        yield Request(url, callback=self.parse_netflix)

    def parse_netflix(self, response):
        is_duplicated = (len(list(self.collection.find({'url': response.url}, {'_id': 1}))) > 0)
        if is_duplicated:
            if self.crawl_type == 'incremental':
                self.state = 'stop'
            return
        yield {
            'title': first(response.xpath('//h1/text()').extract()),
            'url': response.url,
            'release_year': first(response.css('.item-year').xpath('./text()').extract()),
            'maturity_number': first(response.css('.maturity-number').xpath('./text()').extract()).strip(),
            'duration': first(response.xpath('//span[@class="duration"]//text()').extract()),
            'genre': first(response.css('.item-genre').xpath('./text()').extract()),
            'synopsis': first(response.css('.title-info-synopsis').xpath('./text()').extract()),
            'starring': first(response.xpath('//span[@data-uia="info-starring"]/text()').extract()),
            'creator': first(response.xpath('//span[@data-uia="info-creators"]/text()').extract()),
            'watch_offline': first(response.xpath('//span[@data-uia="more-details-item-download"]/text()').extract()),
            'all_genres': ''.join(response.xpath('//span[@class="more-details-item item-genres"]//text()').extract()),
            'mood': ''.join(response.xpath('//span[@class="more-details-item item-mood-tag"]//text()').extract()),
            'audio': ''.join(response.xpath('//span[@class="more-details-item item-audio"]//text()').extract()),
            'subtitle': ''.join(response.xpath('//span[@class="more-details-item item-subtitle"]//text()').extract()),
            'cast': ', '.join(response.xpath('//span[@class="more-details-item item-cast"]//text()').extract()),
            'n_seasons': len(response.xpath('//select[@data-uia="season-selector"]//text()').extract()) or 1,
            'seasons': response.xpath('//select[@data-uia="season-selector"]//text()').extract(),
            'seasons_release_year': [take_year(i) for i in
                                     response.xpath('//*[@data-uia="season-release-year"]//text()').extract()],
            'n_episodes': [len(i.xpath('.//div[@data-uia="episode"]').extract()) for i in
                           response.xpath('//*[@id="seasons-and-episodes-list-container"]/*')] or 1,
            'episode_durations': [i.xpath('.//span[@data-uia="episode-runtime"]//text()').extract() for i in
                                  response.xpath('//*[@id="seasons-and-episodes-list-container"]/*')] or 'NA'
        }
