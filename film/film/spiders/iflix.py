import pymongo
import scrapy
import json
from scrapy.http import Request
from scrapy.utils.project import get_project_settings


class IflixSpider(scrapy.Spider):
    name = 'iflix'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.iflix
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['iflix.com', 'akamaized.net']
        self.start_urls = [
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.action.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.adventure.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.animation.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.anime.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.biography.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.comedy.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.crime.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.documentary.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.documentary.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.family.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.fantasy.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.horror.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.kids.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.lifestyle.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.mystery.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.reality.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.romance.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.sci-fi.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/tv.thriller.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.action.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.adventure.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.animation.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.anime.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.comedy.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.crime.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.documentary.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.education.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.drama.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.family.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.fantasy.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.horror.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.kids.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.lifestyle.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.mystery.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.reality.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.romance.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.sci-fi.json',
            'https://iflix-data.akamaized.net/5/vn/adults/contents/movies.thriller.json'
        ]

    # download_delay = 1.5
    def parse(self, response):
        if self.state == 'run':
            data = json.loads(response.body)
            for item in data:
                if item.get("categoryName") == 'Movies':
                    yield Request(
                        'https://iflix-data.akamaized.net/5/vn/adults/contents/shows/movies.{}.json'.format(item['id']),
                        callback=self.parse_movie)
                else:
                    yield Request(
                        'https://iflix-data.akamaized.net/5/vn/adults/contents/shows/tv.{}.json'.format(item['id']),
                        callback=self.parse_tv)

    def parse_movie(self, response):
        try:
            data = json.loads(response.body)
            is_duplicated = (len(list(
                self.collection.find({'url': 'https://piay.iflix.com/' + data.get('slug')}, {'_id': 1}))) > 0)
            if is_duplicated:
                if self.crawl_type == 'incremental':
                    self.state = 'stop'
                return
            yield {
                'id': data.get('id'),
                'title': data.get('title').get('en_US'),
                'type': 'movie',
                'tier': data.get('tiers'),
                'description': data.get('description').get('en_US'),
                'synopsis': data.get('synopsis').get('en_US'),
                'actors': data.get('actors'),
                'directors': data.get('directors'),
                'genre': data.get('genre'),
                'subGenre': data.get('subGenre'),
                'imageUrl': data.get('imageUrl'),
                'duration': data.get('duration'),
                'url': 'https://piay.iflix.com/' + data.get('slug'),
                'seasons': '',
                'n_episode': '',
                'api_url': response.url
            }
        except:
            pass

    def parse_tv(self, response):
        try:
            data = json.loads(response.body)
            is_duplicated = (len(list(
                self.collection.find({'url': 'https://piay.iflix.com/' + data.get('slug')}, {'_id': 1}))) > 0)
            if is_duplicated:
                if self.crawl_type == 'incremental':
                    self.state = 'stop'
                return
            yield {
                'id': data.get('id'),
                'title': data.get('title').get('en_US'),
                'type': 'tv',
                'tier': data.get('tiers'),
                'description': data.get('description').get('en_US'),
                'synopsis': data.get('synopsis').get('en_US'),
                'actors': data.get('actors'),
                'directors': data.get('directors'),
                'genre': data.get('genre'),
                'subGenre': data.get('subGenre'),
                'imageUrl': data.get('imageUrl'),
                'duration': '',
                'url': 'https://piay.iflix.com/' + data.get('slug'),
                'seasons': len(data.get('seasons')),
                'n_episode': {str(season['seasonNumber']): len(season['episodes']) for season in data.get('seasons')},
                'api_url': response.url
            }
        except:
            pass
