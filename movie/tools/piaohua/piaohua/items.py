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
    update_time = scrapy.Field()        # gengxin shijian
    pic_url = scrapy.Field()            # tupian de dizhi
    link_url = scrapy.Field()           # juji de url
    type = scrapy.Field()               # fenlei