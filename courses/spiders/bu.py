from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from courses.items import Course


class EduSpider(CrawlSpider):
    name = 'bu.edu'
    allowed_domains = ['bu.edu']
    start_urls = ['http://www.bu.edu/academics/']

    rules = (
        Rule(LxmlLinkExtractor(
             allow=('.*/academics/[a-z][a-z][a-z]/courses/[a-z][a-z][a-z]-[a-z][a-z]-[0-9][0-9][0-9]/', ),
        ), callback='parse_item'),

        Rule(LxmlLinkExtractor(
            allow=('.*/academics/[a-z][a-z][a-z]/', '.*/academics/[a-z][a-z][a-z]/courses/.*'),
        )),
    )

    def parse_item(self, response):
        item = Course()
        item["institute"] = 'Boston University'
        item['site'] = 'www.bu.edu'
        item['title'] = response.xpath('//*[@id="col1"]/div/h1/text()').extract()[0]
        item['id'] = response.xpath('//*[@id="col1"]/div/h2/text()').extract()[0]
        item['credits'] = response.xpath('//*[@id="info-box"]/dl/dd[1]/text()').extract()[0]
        item['description'] = response.xpath('//*[@id="course-content"]/p[1]/text()').extract()[0]
        yield item
