import scrapy
from p_test.items import DmozItem
from scrapy import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        sites = sel.xpath("//div[@id='site-list-content']//div[@class='title-and-desc']")
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/div[@class="site-title"]/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('div/text()').extract()
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