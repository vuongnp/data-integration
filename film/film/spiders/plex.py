import pymongo
import scrapy
import json
from scrapy.http import Request
from scrapy.utils.project import get_project_settings


# Lưu ý: Cần thay đổi token thủ công khi crawl


def first(x):
    if len(x) == 0:
        return ''
    else:
        return x[0]


class PlexSpider(scrapy.Spider):
    name = 'plex'

    def __init__(self, crawl_type='all', **kwargs):
        super().__init__(**kwargs)
        settings = get_project_settings()
        self.client = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.client.film
        self.collection = self.db.plex
        self.state = 'run'
        self.crawl_type = crawl_type

        self.allowed_domains = ['plex.tv']
        query = "https://vod.provider.plex.tv/library/sections/movies/all?genre={}&type=99&sort=ratingCount:desc&includeCollections=1&includeExternalMedia=1&X-Plex-Product=Plex%20Web&X-Plex-Version=4.57.2&X-Plex-Client-Identifier=u5j1tqqoo3qbydmdrxuaf5a8&X-Plex-Platform=Chrome&X-Plex-Platform-Version=90.0&X-Plex-Sync-Version=2&X-Plex-Features=external-media%2Cindirect-media&X-Plex-Model=hosted&X-Plex-Device=Windows&X-Plex-Device-Screen-Resolution=1366x286%2C1366x768&X-Plex-Container-Start={}&X-Plex-Container-Size=200&X-Plex-Token=CqShrPEdbo-vnqaUzzy-&X-Plex-Provider]-Version=3.2&X-Plex-Text-Format=plain&X-Plex-Drm=widevine&X-Plex-Language=en"
        self.start_urls = [
            query.format('5f17675407012c0040e5804e', '0'),  # Action/Adventure
            query.format('5d9c046c3c3f87001f33fbfc', '0'),  # Animation
            query.format('5d9c046c705e7a001e6c8d99', '0'),  # Comedy
            query.format('5d9c046c08fddd001f28ab90', '0'),  # Crime
            query.format('5d9c046c705e7a001e6c8da3', '0'),  # Documentary
            query.format('5d9c046c705e7a001e6c8d9a', '0'),  # Drama
            query.format('5d9c046c7b5c2e001e64c612', '0'),  # Horror
            query.format('5d9c046d3c3f87001f33fc20', '0'),  # Musical
            query.format('5d9c046c705e7a001e6c8d9b', '0'),  # Romance
            query.format('5d9c046c2192ba001f2ff6c4', '0'),  # Sci-Fi
            query.format('5d9c046c2192ba001f2ff6c5', '0'),  # Thriller
            query.format('5d9c046cba6eb9001fb93d49', '0'),  # Western
        ]

    # download_delay = 1.5
    def parse(self, response):
        if self.state == 'run':
            size = first(response.xpath('/MediaContainer/@size').extract())
            if size != '0' and size != '':
                for item in response.xpath('/MediaContainer/*'):
                    is_duplicated = (len(list(
                        self.collection.find({'url': first(item.xpath('./@publicPagesURL').extract())},
                                             {'_id': 1}))) > 0)
                    if is_duplicated:
                        if self.crawl_type == 'incremental':
                            self.state = 'stop'
                        continue
                    if first(item.xpath('name()').extract()) == 'Video':
                        yield {
                            'title': first(item.xpath('./@title').extract()),
                            'type': first(item.xpath('./@type').extract()),
                            'thumb': first(item.xpath('./@thumb').extract()),
                            'summary': first(item.xpath('./@summary').extract()),
                            'duration_ms': first(item.xpath('./@duration').extract()),
                            'url': first(item.xpath('./@publicPagesURL').extract()),
                            'contentRating': first(item.xpath('./@contentRating').extract()),
                            'studio': first(item.xpath('./@studio').extract()),
                            'year': first(item.xpath('./@year').extract()),
                            'actors': item.xpath('./Role/@tag').extract(),
                            'directors': item.xpath('./Director/@tag').extract(),
                            'producers': item.xpath('./Producer/@tag').extract(),
                            'writers': item.xpath('./Writer/@tag').extract(),
                            'genres': item.xpath('./Genre/@tag').extract()
                        }
                    if first(item.xpath('name()').extract()) == 'Directory':
                        yield {
                            'title': first(item.xpath('./@title').extract()),
                            'type': first(item.xpath('./@type').extract()),
                            'thumb': first(item.xpath('./@thumb').extract()),
                            'summary': first(item.xpath('./@summary').extract()),
                            'url': first(item.xpath('./@publicPagesURL').extract()),
                            'contentRating': first(item.xpath('./@contentRating').extract()),
                            'studio': first(item.xpath('./@studio').extract()),
                            'year': first(item.xpath('./@year').extract()),
                            'actors': item.xpath('./Role/@tag').extract(),
                            'directors': item.xpath('./Director/@tag').extract(),
                            'producers': item.xpath('./Producer/@tag').extract(),
                            'writers': item.xpath('./Writer/@tag').extract(),
                            'genres': item.xpath('./Genre/@tag').extract()
                        }
                offset = int(first(response.xpath('/MediaContainer/@offset').extract()))
                s = 'X-Plex-Container-Start={}'
                new_link=response.url.replace(s.format(offset), s.format(offset + 200))
                yield Request(new_link)
