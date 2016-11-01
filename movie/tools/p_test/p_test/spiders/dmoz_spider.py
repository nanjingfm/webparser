import scrapy
from p_test.items import DmozItem
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider

class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = [".piaohua.com/"]
    start_urls = [
        "http://www.piaohua.com/"
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        sites = sel.xpath("//div[@id='main']//ul/li")
        items = []
        print(len(sites))
        for site in sites:
            item = DmozItem()
            item['name'] = self.getName(site)
            item['link'] = self.getLink(site)
            item['updatetime'] = self.getUpdateTime(site)
            item['imageurl'] = self.getImageUrl(site)
            items.append(item)
        return items

    def getImageUrl(self, item):
        imageurl = item.xpath("a[@class='img']/img/@src").extract()
        if imageurl:
            return imageurl[0]
        else:
            return ''

    def getLink(self, item):
        link = item.xpath("a[@class='img']/@href").extract()
        if link:
            return link[0]
        else:
            return ''

    def getUpdateTime(self, item):
        updatetime = item.xpath("span/text()").extract()
        if updatetime:
            return updatetime[0]
        else:
            return item.xpath("span/font/text()").extract()[0]

    def getName(self, item):
        name = item.xpath("a/strong/font/font/text()").extract()
        if name:
            return name[0]
        else:
            return item.xpath("a/strong/font/text()").extract()[0]