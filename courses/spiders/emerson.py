from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from courses.items import Course


class EduSpider(CrawlSpider):
    name = 'emerson.edu'
    allowed_domains = ['emerson.edu']
    start_urls = ['http://www.emerson.edu/academics/courses/descriptions']

    def parse(self, response):
		sel = Selector(response)

		courseSelector = '//ul[@id="courseList"]//li'
		courses = sel.xpath(courseSelector)

		for course in courses:
			item = Course()
			item['title'] = course.xpath('div//div//strong')
			yield item

