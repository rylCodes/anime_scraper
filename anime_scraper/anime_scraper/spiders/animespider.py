import scrapy
from anime_scraper.items import AnimeScraperItem
import random

class AnimespiderSpider(scrapy.Spider):
    name = "animespider"
    allowed_domains = ["aniwave.to"]
    start_urls = ["https://aniwave.to/az-list"]

    custom_settings = {
        'FEEDS': {
            'animesdata.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        animes = response.css('div.item')
        for anime in animes:
            relative_url = anime.css('div.poster a').attrib['href']
            anime_url = "https://aniwave.to" + relative_url
            yield response.follow(anime_url, callback=self.parse_anime_page)

        next_page_url = response.css('a[rel="next"] ::attr(href)')
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    # def parse_anime_page(self, response):
    #     bmeta_first_child = response.css('div.bmeta > div:nth-child(1)')
    #     bmeta_second_child = response.css('div.bmeta > div:nth-child(2)')
    #     yield {
    #         'poster': response.css('div.poster img::attr(src)').get(),
    #         'title': response.css('div.info h1.title::text').get(),
    #         'sypnosis': response.css('div.content::text').getall(),
    #         'type': bmeta_first_child.css('div.meta > div:nth-child(1) a::text').get(),
    #         'genre': bmeta_first_child.css('div.meta > div:nth-child(7) a::text').getall(),
    #         'duration': bmeta_second_child.css('div.meta > div:nth-child(2) span::text').get(),
    #         'episodes': bmeta_second_child.css('div.meta > div:nth-child(3) span::text').get(),
    #     }

    def parse_anime_page(self, response):
        bmeta_first_child = response.css('div.bmeta > div:nth-child(1)')
        bmeta_second_child = response.css('div.bmeta > div:nth-child(2)')
        anime_item = AnimeScraperItem()

        anime_item['url'] = response.url
        anime_item['title'] = response.css('div.info h1.title::text').get()
        anime_item['poster'] = response.css('div.poster img::attr(src)').get()
        anime_item['sypnosis'] = response.css('div.content::text').getall()
        anime_item['type'] = bmeta_first_child.css('div.meta > div:nth-child(1) a::text').get()
        anime_item['genre'] = bmeta_first_child.css('div.meta > div:nth-child(7) a::text').getall()
        anime_item['duration'] = bmeta_second_child.css('div.meta > div:nth-child(2) span::text').get()
        anime_item['episodes'] = bmeta_second_child.css('div.meta > div:nth-child(3) span::text').get()

        yield anime_item