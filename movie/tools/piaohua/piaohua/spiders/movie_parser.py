import re
import urllib2

import scrapy
from piaohua.items import PiaohuaItem
from scrapy.http import Request
from scrapy import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

class PiaohuaCrawlSpider(CrawlSpider):
    name = "PiaohuaCrawlSpider"
    allowed_domains = ['piaohua.com']
    start_urls = [
        'http://piaohua.com/html/aiqing/index.html',
        'http://piaohua.com/html/kehuan/index.html',]
    rules = [
        Rule(SgmlLinkExtractor(allow=('list_'),
                               restrict_xpaths=("//div[@class='page']/a")),
             callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        # print "parse_item>>>>>>"
        items = []
        sel = Selector(response)
        movie_list = sel.xpath("//div[@id='nml']//dl")
        for movie in movie_list:
            item = PiaohuaItem()
            item['linkurl'] = self.getLinkUrl(movie)
            item['name'] = self.getName(movie)
            item['imageurl'] = self.getImageUrl(movie)
            item['type'] = self.getType(response)

            movieDetail = self.getMovieDetail(item['linkurl'])
            # item['downloadlink'] = self.getDownloadLink(movieDetail)
            # item['updatetime'] = self.getUpdateTime(movieDetail)
            items.append(item)
        return items

    def getLinkUrl(self, site):
        return site.xpath("dt/a/@href").extract()[0]

    def getImageUrl(self, site):
        return site.xpath("dt//img/@src").extract()[0]

    def getName(self, site):
        return site.xpath("dd/strong/a/b/font/text()").extract()[0]

    def getType(self, response):
        return response.url.split('/')[-2]

    def getUpdateTime(self, site):
        str = site.xpath("//div[@id='show']/div[@id='showdesc']/text()").extract()[0]
        return re.search(r'.*(\d{4}-\d{2}-\d{2}).*', str).group(1)

    def getDownloadLink(self, site):
        return site.xpath("//anchor/a/text()").extract()

    def getMovieDetail(self, url):
        url = 'http://piaohua.com' + url
        return Selector(Request(url=url))