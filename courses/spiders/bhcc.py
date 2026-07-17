from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from courses.items import Course


class EduSpider(CrawlSpider):
    name = "bhcc.mass.edu"
    allowed_domains = ["bhcc.mass.edu"]
    start_urls = ["http://www.bhcc.mass.edu/catalog/courses/index.php"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r".*/catalog/courses/index.php\?dept=[A-Z][A-Z][A-Z]",),
            ),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(
                allow=(".*/catalog/courses/.*",),
            )
        ),
    )

    def parse_item(self, response):
        container = response.xpath('//*[@id="mainContentArea"]/div')
        for div in container:
            item = Course()
            item["site"] = "www.bhcc.mass.edu"
            item["institute"] = "Bunker Hill Community College"
            item["title"] = div.xpath('div[@class="classHeader"]/div[@class="courseTitle"]/text()').get()
            item["id"] = div.xpath('div[@class="classHeader"]/div[@class="courseNum"]/text()').get()
            credits = div.xpath('div[@class="classHeader"]/div[@class="courseCredits"]/text()').get()
            item["credits"] = credits[0] if credits else None
            item["description"] = div.xpath('div[@class="courseDescription"]/p/text()').get()
            item["category"] = div.xpath('//*[@id="mainContentArea"]/h1/text()').get()
            yield item
