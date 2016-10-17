from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from courses.items import Course


class EduSpider(CrawlSpider):
    name = 'emerson.edu'
    allowed_domains = ['emerson.edu']
    start_urls = ['http://www.emerson.edu/academics/']


    def parse_item(self, response):
        item = Course()
        item["institute"] = 'Emerson College'
        item['site'] = 'www.emerson.edu'
        item['title'] = response.xpath('//*[@id="BC110"]/div[1]/strong').extract()[0]
        item['id'] = response.xpath('//*[@id="BC110"]/div[1]/strong').extract()[0]
        item['credits'] = response.xpath('//*[@id="BC110"]/div[1]/em').extract()[0]
        item['description'] = response.xpath('//*[@id="BC110"]/div[2]').extract()[0]
        yield item