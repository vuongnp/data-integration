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


class ImdbSpider(scrapy.Spider):
    name = 'imdb'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.imdb
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['imdb.com']
        self.start_urls = [
            'https://www.imdb.com/search/title/?title_type=feature,tv_series&release_date=1970-01-01,&languages=en&moviemeter=,20000&adult=include&view=simple&count=250']

    # download_delay = 1.5
    def parse(self, response):
        if self.state == 'run':
            for film in response.xpath('//div[@class="lister-list"]/div/div/a/@href').extract():
                yield Request('https://www.imdb.com' + film, callback=self.parse_imdb)
            yield Request('https://www.imdb.com' + first(response.xpath('//a[text()="Next »"]/@href').extract()))

    def parse_imdb(self, response):
        is_duplicated = (len(list(self.collection.find({'url': response.url}, {'_id': 1}))) > 0)
        if is_duplicated:
            if self.crawl_type == 'incremental':
                self.state = 'stop'
            return
        result = {
            'title': first(response.xpath('//h1//text()').extract()).strip(),
            'url': response.url,
            'duration': first(response.xpath('//h1/..//time/text()').extract()).strip(),
            'genre': response.xpath('//h1/../div/a[contains(@href,"genres")]/text()').extract(),
            'releaseinfo': first(
                response.xpath('//h1/../div/a[contains(@href,"releaseinfo")]/text()').extract()).strip(),
            'rating': first(response.xpath('//span[@itemprop="ratingValue"]/text()').extract()),
            'rating_count': first(response.xpath('//span[@itemprop="ratingCount"]/text()').extract()),
            'poster': first(response.xpath('//div[@class="poster"]/a/img/@src').extract()),
            'summary': first(response.xpath('//div[@class="summary_text"]/text()').extract()).strip(),
            'creator': response.xpath('//h4[text()="Creator:"]/../a/text()').extract(),
            'stars': response.xpath('//h4[text()="Stars:"]/../a[contains(@href,"/name/")]/text()').extract(),
            'Director': response.xpath('//h4[text()="Director:"]/../a[contains(@href,"/name/")]/text()').extract(),
            'writers': response.xpath('//h4[text()="Writers:"]/../a[contains(@href,"/name/")]/text()').extract(),
            'popularity': first(first(response.xpath(
                '//div[@class="titleReviewBar "]//div[contains(text(),"Popularity")]/../div[2]/span/text()').extract()).split())
        }
        n_seasons = first(response.xpath('//div[@class="seasons-and-year-nav"]//a/text()').extract())
        if n_seasons.isdigit() and int(n_seasons) < 100:
            n_seasons = int(n_seasons)
            result['n_seasons'] = n_seasons
            result['n_episodes'] = {}
            link = re.match(r'(https://www.imdb.com/title/.*?/)', response.url).group(1)
            for i in range(1, n_seasons + 1):
                r = requests.get(link + 'episodes?season={}&ref_=tt_eps_sn_{}'.format(i, i))
                soup = BeautifulSoup(r.content, 'lxml')
                result['n_episodes']['Season ' + str(i)] = len(soup.find_all('div', 'list_item'))
        else:
            result['n_seasons'] = ''
            result['n_episodes'] = ''
        yield result
