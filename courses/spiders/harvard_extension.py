from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from courses.items import Course


class EduSpider(CrawlSpider):
    name = "extension.harvard.edu"
    allowed_domains = ["extension.harvard.edu"]
    start_urls = ["http://www.extension.harvard.edu/academics/courses/course-catalog"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(".*/academics/courses/.*/[0-9][0-9][0-9][0-9][0-9]",),
            ),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(
                allow=(".*/academics/courses/.*",),
            )
        ),
    )

    def parse_item(self, response):
        item = Course()
        item["institute"] = "Harvard University Extension School"
        item["site"] = "www.extension.harvard.edu"
        item["title"] = response.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[1]/h1/text()').get()
        item["id"] = response.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[2]/div/p/span/text()').get()
        item["credits"] = response.xpath('//*[@id="main"]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/p/text()').get()[0]
        item["description"] = response.xpath('//*[@id="main"]/div/div/div[1]/div[1]/div[3]/div/p/text()').get()
        yield item
