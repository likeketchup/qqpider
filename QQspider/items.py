# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    urls = scrapy.Field()
    title = scrapy.Field()
    catalog = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    first_graph = scrapy.Field()
    img = scrapy.Field()
    pass
