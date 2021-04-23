import scrapy

from scrapy.loader import ItemLoader

from ..items import IsdbarItem
from itemloaders.processors import TakeFirst


class IsdbarSpider(scrapy.Spider):
	name = 'isdbar'
	start_urls = ['https://www.isdb.org/ar/news']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="field-title"]/h1/text()').get()
		description = response.xpath('//div[@class="field field--name-field-text field--type-text-long field--label-hidden field--item"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//header//time/text()').get()

		item = ItemLoader(item=IsdbarItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
