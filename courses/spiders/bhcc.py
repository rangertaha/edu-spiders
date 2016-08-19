
from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from courses.items import Course


class EduSpider(CrawlSpider):
    name = 'bhcc.mass.edu'
    allowed_domains = ['bhcc.mass.edu']
    start_urls = ['http://www.bhcc.mass.edu/catalog/courses/index.php']

    rules = (
        Rule(LxmlLinkExtractor(
             allow=('.*/catalog/courses/index.php\?dept=[A-Z][A-Z][A-Z]', ),
        ), callback='parse_item'),

        Rule(LxmlLinkExtractor(
            allow=('.*/catalog/courses/.*',),
        )),
    )

    def parse_item(self, response):
        container = response.xpath('//*[@id="mainContentArea"]/div')
        for div in container:
            item = Course()
            item['site'] = 'www.bhcc.mass.edu'
            item["institute"] = "Bunker Hill Community College"
            item['title'] = div.xpath('div[@class="classHeader"]/div[@class="courseTitle"]/text()').extract()[0]
            item['id'] = div.xpath('div[@class="classHeader"]/div[@class="courseNum"]/text()').extract()[0]
            item['credits'] = div.xpath('div[@class="classHeader"]/div[@class="courseCredits"]/text()').extract()[0][0]
            item['description'] = div.xpath('div[@class="courseDescription"]/p/text()').extract()[0]
            item['category'] = div.xpath('//*[@id="mainContentArea"]/h1/text()').extract()[0]
            yield item
