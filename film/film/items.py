# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst

class FilmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# class NetflixItem(scrapy.Item):
#     title=Field(output_processor=TakeFirst())
#     url
#     release_year
#     genre
#     synopsis
#     starring
#     creator
#     watch_offline
#     all_genres
#     mood
#     audio
#     subtitle
#     cast
#     n_seasons
#     seasons
#     seasons_release_year
#     n_episodes
