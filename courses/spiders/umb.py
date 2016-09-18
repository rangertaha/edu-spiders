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
            allow=('.*/academics/course_catalog/course_info/[a-z]+_[A-Z]+_all_[0-9]+',),
        ), callback='parse_item'),

        Rule(LxmlLinkExtractor(
            allow=(
            '.*/academics/course_catalog/listing/[a-z]+', '/academics/course_catalog/courses/[a-z]+_[A-Z]+_all$'),
        )),
    )

    def clean(self, data):
        if len(data) > 0:
            if isinstance(data, list):
                return data[0]

    def parse_item(self, response):
        item = Course()
        item["institute"] = 'University of Massachusetts Boston'
        item['site'] = 'www.umb.edu'
        item['title'] = response.xpath('//*[@id="pageTitle"]/text()').extract()[0]
        breadcrumb = response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/text()').extract()[0]
        b = breadcrumb.replace('>', ' ')
        b = b.replace('UGRD', '')
        b = b.replace('GRAD', '')
        item['id'] = b.strip()
        item['credits'] = self.clean(response.xpath('//*[@id="content"]/div[2]/div[2]/table[1]/tbody/tr[2]/td/div/div[6]/span[2]/text()').extract())
        item['description'] = response.xpath('//*[@id="content"]/div[2]/div[2]/p[2]/text()').extract()[0]
        yield item
