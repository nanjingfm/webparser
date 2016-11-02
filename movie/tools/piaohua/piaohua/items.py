# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PiaohuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()               # jujide mingcheng
    updatetime = scrapy.Field()        # gengxin shijian
    imageurl = scrapy.Field()            # tupian de dizhi
    linkurl = scrapy.Field()           # juji de url
    downloadlink = scrapy.Field()           # juji de url
    type = scrapy.Field()               # fenlei