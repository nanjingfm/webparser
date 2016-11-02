import scrapy
from p_test.items import DmozItem
from scrapy import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

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

class CSDNBlogCrawlSpider(CrawlSpider):
    name = "CSDNBlogCrawlSpider"
    allowed_domains = ['blog.csdn.net']
    start_urls = ['http://blog.csdn.net/u012150179/article/details/11749017']
    rules = [
        Rule(SgmlLinkExtractor(allow=('/u012150179/article/details'),
                               restrict_xpaths=('//li[@class="next_article"]')),
             callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        # print "parse_item>>>>>>"
        item = {}
        sel = Selector(response)
        blog_url = str(response.url)
        blog_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()

        item['blog_name'] = [n.encode('utf-8') for n in blog_name]
        item['blog_url'] = blog_url.encode('utf-8')

        yield item
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
