import scrapy
import urllib
import requests

class DmozItem(scrapy.Item):
	Title = scrapy.Field()
	Company_name = scrapy.Field()
	Location = scrapy.Field()
	Salary = scrapy.Field()
	Job_type = scrapy.Field()
	Industry = scrapy.Field()
	Company_size = scrapy.Field()
	Job_function = scrapy.Field()
	Img_Url = scrapy.Field()


class DmozSpider(scrapy.Spider):
	name = "glass"
	page_numbers = 1
	start_urls = [
    'https://www.glassdoor.com/Job/bismarck-jobs-SRCH_IL.0,8_IC1156224.htm'
    ]
	BASE_URL = 'https://www.glassdoor.com'

	def parse(self, response):
		links = response.css('a.jobLink').xpath("@href").extract()
		for link in links:
			absolute_url = self.BASE_URL + link
			yield scrapy.Request(absolute_url,callback=self.parse_attr)
		next_page = self.BASE_URL + response.css('li.css-1yshuyv a').xpath("@href").extract()
		print("next_page")
		if next_page:
				yield Scarpy.Request(next_page,callback=self.parse_attr)
		else:
			print("Finish")
	def parse_attr(self, response):
		item = DmozItem()
		title = response.css('div.css-17x2pwl::text').extract()
		company_name = response.css('div.css-16nw49e::text').extract()
		location = response.css('div.css-1v5elnn::text').extract()
		salary = response.css('span.small::text').extract()
		data = response.css('span.css-sr4ps0::text').extract()
		job_type = data[0]
		industry = data[1]
		company_size = data[2]
		job_function = response.css('span.css-o4d739::text').extract()
		data_img = response.css('img.lazy').xpath("@data-original").extract()
		try:
			img = data_img[1]
		except IndexError:
			img =""
		item['Title'] = title
		item['Company_name'] = company_name
		item['Location'] = location
		item['Salary'] = salary
		item['Job_type'] = job_type
		item['Industry'] = industry
		item['Company_size'] = company_size
		item['Job_function'] = job_function
		item['Img_Url'] = img
		return item
        
		