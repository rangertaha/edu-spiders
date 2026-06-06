from scrapy import Spider

from courses.items import Course


class EduSpider(Spider):
    name = "emerson.edu"
    allowed_domains = ["emerson.edu"]
    start_urls = ["http://www.emerson.edu/academics/courses/descriptions"]

    def parse(self, response):
        for li in response.xpath('//ul[@id="courseList"]/li'):
            item = Course()
            item["site"] = "www.emerson.edu"
            item["institute"] = "Emerson College"
            item["title"] = li.xpath("div/div[1]/strong/text()").get()
            item["description"] = li.xpath("div/div[2]").get()
            item["credits"] = li.xpath("div/div[1]/em/text()").get()
            item["id"] = li.xpath("@data-id").getall()
            item["category"] = li.xpath("@data-deptcode").getall()
            yield item
