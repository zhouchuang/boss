# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    jobName = scrapy.Field()
    salary = scrapy.Field()
    companyName = scrapy.Field()
    city = scrapy.Field()
    life = scrapy.Field()
    education = scrapy.Field()
    skill = scrapy.Field()
    time = scrapy.Field()
