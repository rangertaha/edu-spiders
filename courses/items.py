# -*- coding: utf-8 -*-
import scrapy


class Course(scrapy.Item):
    site = scrapy.Field()
    institute = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    credits = scrapy.Field()
    category = scrapy.Field()
