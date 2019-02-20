# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AzichanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #list content
    id = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    transferor = scrapy.Field()
    transferee = scrapy.Field()
    assets = scrapy.Field()
    detailUrl = scrapy.Field()
    #debet detail
    debetNumber = scrapy.Field()
    debetIntroduction = scrapy.Field()
