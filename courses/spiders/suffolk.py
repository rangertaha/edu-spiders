from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from courses.items import Course


class EduSpider(CrawlSpider):
    name = "suffolk.edu"
    allowed_domains = ["suffolk.edu"]
    start_urls = ["http://www.suffolk.edu/college/departments.php"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r".*/college/departments/[0-9][0-9][0-9][0-9][0-9]\.php",),
            ),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(
                allow=(".*/college/departments/.*",),
            )
        ),
    )

    def parse_item(self, response):
        container = response.xpath('//ul[@id="a_course_0"]/li')
        for li in container:
            item = Course()
            item["institute"] = "Suffolk University"
            item["site"] = "www.suffolk.edu"

            item["title"] = li.xpath("h2/text()").get()
            item["id"] = li.xpath("h2/text()").re_first(r"^([A-Z]+-[0-9]+).*")

            il = li.xpath('div[@class="item"]/*')
            for _ in range(len(il)):
                if len(il) > 2:
                    p = il.pop()
                    h = il.pop()

                    header = h.xpath("text()").get()
                    para = p.xpath("text()").get()
                    if "Prerequisites:" in header:
                        pass
                    if "Credits" in header:
                        item["credits"] = float(para)

                    if "Description" in header:
                        item["description"] = para

                    if "Type" in header:
                        item["category"] = para
            # if item['id'] and item['title'] and item['description']:
            yield item
