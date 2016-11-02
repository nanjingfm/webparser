import scrapy
from piaohua.items import PiaohuaItem
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
            item['link_url'] = movie.xpath("dt/a/@href").extract();
            items.append(item)
        return items

    def getMovieDetail(self, url):
        pass