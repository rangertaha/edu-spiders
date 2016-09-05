from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from courses.items import Course


class EduSpider(CrawlSpider):
    name = 'suffolk.edu'
    allowed_domains = ['suffolk.edu']
    start_urls = ['http://www.suffolk.edu/college/departments.php']

    rules = (
        Rule(LxmlLinkExtractor(
             allow=('.*/college/departments/[0-9][0-9][0-9][0-9][0-9].php', ),
        ), callback='parse_item'),

        Rule(LxmlLinkExtractor(
            allow=('.*/college/departments/.*', ),
        )),
    )

    def parse_item(self, response):
        container = response.xpath('//ul[@id="a_course_0"]/li')
        for li in container:
            item = Course()
            item["institute"] = 'Suffolk University'
            item['site'] = 'www.suffolk.edu'

            item['title'] = li.xpath('h2/text()').extract()[0]
            item['id'] = li.xpath('h2/text()').re(r'^([A-Z]+-[0-9]+).*')[0]


            il = li.xpath('div[@class="item"]/*')
            for n in range(len(il)):
                if len(il) > 2:
                    p = il.pop()
                    h = il.pop()

                    header = h.xpath('text()').extract()[0]
                    para = p.xpath('text()').extract()[0]
                    if 'Prerequisites:' in header:
                        pass
                    if 'Credits' in header:
                        item['credits'] = float(para)

                    if 'Description' in header:
                        item['description'] = para

                    if 'Type' in header:
                        item['category'] = para
            #if item['id'] and item['title'] and item['description']:
            yield item
