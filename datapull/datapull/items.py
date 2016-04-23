# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YahooItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    symbol = scrapy.Field()
    dates = scrapy.Field()
    opens = scrapy.Field()
    highs = scrapy.Field()
    lows =  scrapy.Field()
    closes = scrapy.Field()
    volumes = scrapy.Field()
    adjcloses = scrapy.Field()
    exchange = scrapy.Field()