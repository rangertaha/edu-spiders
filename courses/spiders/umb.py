from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from courses.items import Course


class EduSpider(CrawlSpider):
    name = 'umb.edu'
    allowed_domains = ['umb.edu']
    start_urls = ['https://www.umb.edu/academics/course_catalog']

    rules = (
        Rule(LxmlLinkExtractor(
             allow=('.*/academics/course_catalog/courses/[a-z]+_[A-Z]+', 'https://www.umb.edu/academics/course_catalog/course_info/grd_AMST_all_604'),
        ), callback='parse_item'),

        Rule(LxmlLinkExtractor(
            allow=('.*/academics/course_catalog/courses/.*', ),
        )),
    )

    def parse_item(self, response):
        item = Course()
        item["institute"] = 'Harvard University Extension School'
        item['site'] = 'www.umb.edu'
        item['title'] = response.xpath('//*[@id="content"]/div[2]/div[2]/ul/li[4]/h4/text()').extract()[0]
        item['id'] = response.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div/p/span/text()').extract()[0]
        item['credits'] = response.xpath('//*[@id="main"]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/p/text()').extract()[0][0]
        item['description'] = response.xpath('//*[@id="content"]/div[2]/div[2]/ul/li[4]/div/text()').extract()[0]
        yield item
