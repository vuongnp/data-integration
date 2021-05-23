import pymongo
import scrapy
import json
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
import re
from bs4 import BeautifulSoup
import requests
import re


def first(x):
    if len(x) == 0:
        return ''
    else:
        return x[0]


def get_n_episodes(links):
    res = {}
    for link in links:
        r = requests.get("https://www.primevideo.com/" + link)
        soup = BeautifulSoup(r.content, 'lxml')
        res[soup.find('label', attrs={'for': 'av-droplist-av-atf-season-selector'}).text] = int(
            re.match(r'Episodes \((\d*)\)', soup.find(id="tab-content-episodes").h1.text).group(1))
    return res


def get_n_episodes_origin(link):
    res = {}
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    res[soup.find('h1', attrs={'data-automation-id': 'title'}).text] = int(
        re.match(r'Episodes \((\d*)\)', soup.find(id="tab-content-episodes").h1.text).group(1))
    return res


def get_title(s):
    res = re.match(r'(Prime Video: )?(?P<name>.+) (-|–) Season [\d]', s, re.IGNORECASE)
    if res is None:
        res = re.match(r'(Prime Video: )?(?P<name>.+) Season [\d]', s, re.IGNORECASE)
        if res is None:
            res = re.match(r'(Prime Video: )?(?P<name>.+)', s)
            if res is None:
                return ''
    return res.group('name')


class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.amazon
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['primevideo.com', 'justwatch.com']
        query = 'https://apis.justwatch.com/content/titles/en_PH/popular?body={"fields":["full_path"],"genres":["%s"],"providers":["prv"],"enable_provider_filter":false,"monetization_types":[],"page":1,"page_size":3,"matching_offers_only":true}&language=en'
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
        url = response.xpath('//*[@alt="Amazon Prime Video"]/../@href').extract()[0]
        yield Request(url, callback=self.parse_amazon)

    def parse_amazon(self, response):
        is_duplicated = (len(list(self.collection.find({'url': response.url}, {'_id': 1}))) > 0)
        if is_duplicated:
            if self.crawl_type == 'incremental':
                self.state = 'stop'
            return
        n_episode = first(response.xpath('//*[@id="tab-content-episodes"]//h1/text()[3]').extract())
        if n_episode == '':
            n_episode_origin = {}
        else:
            n_episode_origin = {
                first(response.xpath('//span[contains(text(),"Season ")]/text()').extract()): int(n_episode)}
        yield {
            'title': get_title(first(response.xpath('//head/title/text()').extract())),
            'url': response.url,
            'release_year': first(response.xpath('//*[@data-automation-id="release-year-badge"]/text()').extract()),
            'maturity_number': first(response.xpath('//*[@data-automation-id="rating-badge"]//text()').extract()),
            'duration': first(response.xpath('//span[@data-automation-id="runtime-badge"]//text()').extract()),
            'genres': response.xpath(
                '//*[@id="meta-info"]//span[text()="Genres"]/parent::*/following-sibling::*//a/text()').extract(),
            'director': response.xpath(
                '//*[@id="meta-info"]//span[text()="Directors"]/parent::*/following-sibling::*//a/text()').extract(),
            'starring': response.xpath(
                '//*[@id="meta-info"]//span[text()="Starring"]/parent::*/following-sibling::*//a/text()').extract(),
            'description': first(response.xpath('//div[@dir="auto"]/text()').extract()),
            'seasons': list(
                dict.fromkeys(response.xpath('//body//ul/li/a/span[contains(text(),"Season")]/text()').extract())),
            'n_episodes': (get_n_episodes(
                response.xpath(
                    '//body//ul/li/a/span[contains(text(),"Season")]/parent::*/@href').extract()) | n_episode_origin)
        }
