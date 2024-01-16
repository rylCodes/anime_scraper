# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeScraperItem(scrapy.Item):
    url = scrapy.Field()
    poster = scrapy.Field()
    title = scrapy.Field()
    sypnosis = scrapy.Field()
    type = scrapy.Field()
    genre = scrapy.Field()
    duration = scrapy.Field()
    episodes = scrapy.Field()