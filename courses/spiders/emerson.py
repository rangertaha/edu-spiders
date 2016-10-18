from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from courses.items import Course


class EduSpider(Spider):
    name = 'emerson.edu'
    allowed_domains = ['emerson.edu']
    start_urls = ['http://www.emerson.edu/academics/courses/descriptions']

    def parse(self, response):
        lu = response.xpath('//ul[@id="courseList"]')

        for li in lu:
            item = Course()
            item['title'] = li.xpath('li/div[@id="BC110"]/div[1]/strong/text()').extract()[0]
            yield item

