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
        lu = response.xpath('//ul[@id="courseList"]/li')



        for li in lu:
            item = Course()
            item['site'] = 'www.emerson.edu'
            item["institute"] = "Emerson College"
            item['title'] = li.xpath('div/div[1]/strong/text()').extract()[0]
            item['credits'] = li.xpath('div/div[1]/em/text()').extract()[0]
            item['id'] = li.xpath('@data-id').extract()
            item['category'] = li.xpath('@data-deptcode').extract()
            yield item
