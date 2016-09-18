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
        item['title'] = response.xpath('//*[@id="pageTitle"]/text()').extract()[0]
        breadcrumb = response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/text()').extract()[0]
        b = breadcrumb.replace('>', ' ')
        b = b.replace('UGRD', '')
        b = b.replace('GRAD', '')
        item['id'] = b.strip()
        item['credits'] = response.xpath('//*[@id="content"]/div[2]/div[2]/table[1]/tbody/tr[2]/td/div/div[6]/span[2]/text()').extract()[0]
        item['description'] = response.xpath('//*[@id="content"]/div[2]/div[2]/p[2]/text()').extract()[0]
        yield item
