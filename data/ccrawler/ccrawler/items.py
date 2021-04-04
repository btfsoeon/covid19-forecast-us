# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CcrawlerItem(scrapy.Item):
    date = scrapy.Field()
    state = scrapy.Field()
    county = scrapy.Field()
    vaccination_pct = scrapy.Field()
