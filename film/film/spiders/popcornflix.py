import pymongo
import scrapy
import json
from scrapy.http import Request
from scrapy.utils.project import get_project_settings


class PopcornflixSpider(scrapy.Spider):
    name = 'popcornflix'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.popcornflix
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['popcornflix.com', 'unreel.me']
        self.start_urls = [
            'https://api.unreel.me/v2/sites/popcornflix/channels'
        ]

    # download_delay = 1.5
    def parse(self, response):
        if self.state == 'run':
            data = json.loads(response.body)
            for channel in data:
                yield Request(
                    'https://api.unreel.me/v2/sites/popcornflix/channels/{}/movies?__site=popcornflix&__source=web&page=0&pageSize=10000'.format(
                        channel.get('channelId')),
                    callback=self.parse_movie_channel)
                yield Request(
                    'https://api.unreel.me/v2/sites/popcornflix/channels/{}/series?__site=popcornflix&__source=web&page=0&pageSize=10000'.format(
                        channel.get('channelId')),
                    callback=self.parse_series_channel)

    def parse_movie_channel(self, response):
        try:
            data = json.loads(response.body)
            for item in data['items']:
                try:
                    url = 'https://www.popcornflix.com/movie/' + item['uid']
                    is_duplicated = (len(list(
                        self.collection.find({'url': url}, {'_id': 1}))) > 0)
                    if is_duplicated:
                        if self.crawl_type == 'incremental':
                            self.state = 'stop'
                        continue
                    yield {
                        'title': item.get('title'),
                        'type': 'movie',
                        'description': item.get('description'),
                        'cast': item.get('movieData').get('cast'),
                        'creators': item.get('movieData').get('creators'),
                        'directors': item.get('movieData').get('directors'),
                        'genres': item.get('movieData').get('genres'),
                        'mpaa': item.get('movieData').get('mpaa'),
                        'poster': item.get('movieData').get('poster'),
                        'duration': item.get('contentDetails').get('duration'),
                        'url': url,
                        'seasons': '',
                        'api_url': response.url
                    }
                except:
                    pass
        except:
            pass

    def parse_series_channel(self, response):
        try:
            data = json.loads(response.body)
            for item in data['items']:
                try:
                    url = 'https://www.popcornflix.com/series/' + item['uid']
                    is_duplicated = (len(list(
                        self.collection.find({'url': url}, {'_id': 1}))) > 0)
                    if is_duplicated:
                        if self.crawl_type == 'incremental':
                            self.state = 'stop'
                        continue
                    yield {
                        'title': item.get('title'),
                        'type': 'series',
                        'description': item.get('description'),
                        'cast': item.get('cast'),
                        'creators': item.get('creators'),
                        'directors': item.get('directors'),
                        'genres': item.get('genres'),
                        'mpaa': item.get('mpaa'),
                        'poster': item.get('poster'),
                        'duration': '',
                        'url': url,
                        'seasons': len(item.get('seasons')),
                        'api_url': response.url
                    }
                except:
                    pass
        except:
            pass
