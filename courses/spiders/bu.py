from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from courses.items import Course


class EduSpider(CrawlSpider):
    name = "bu.edu"
    allowed_domains = ["bu.edu"]
    start_urls = ["http://www.bu.edu/academics/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(".*/academics/[a-z][a-z][a-z]/courses/[a-z][a-z][a-z]-[a-z][a-z]-[0-9][0-9][0-9]/",),
            ),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(
                allow=(".*/academics/[a-z][a-z][a-z]/", ".*/academics/[a-z][a-z][a-z]/courses/.*"),
            )
        ),
    )

    def parse_item(self, response):
        item = Course()
        item["institute"] = "Boston University"
        item["site"] = "www.bu.edu"
        item["title"] = response.xpath('//*[@id="col1"]/div/h1/text()').get()
        item["id"] = response.xpath('//*[@id="col1"]/div/h2/text()').get()
        item["credits"] = response.xpath('//*[@id="info-box"]/dl/dd[1]/text()').get()
        item["description"] = response.xpath('//*[@id="course-content"]/p[1]/text()').get()
        yield item
