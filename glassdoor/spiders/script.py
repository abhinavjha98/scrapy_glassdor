import scrapy
import urllib
import requests
from urllib.request import Request, urlopen
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
	apply_link = scrapy.Field()
	Description = scrapy.Field()


class DmozSpider(scrapy.Spider):
	name = "glass"
	page_numbers = 1
	start_urls = [
    'https://www.glassdoor.com/Job/bismarck-jobs-SRCH_IL.0,8_IC1156224.htm'
    ]
	BASE_URL = 'https://www.glassdoor.com'
	

	def parse(self, response):
		i = 1
		pg_links = []
		links = response.css('a.jobLink').xpath("@href").extract()
		for link in links:
			absolute_url = self.BASE_URL + link
			yield scrapy.Request(absolute_url,callback=self.parse_attr,dont_filter=True)
		# next_ =  response.css('li.css-1yshuyv a').xpath("@href").extract()
		# next_page = self.BASE_URL + next_[0]
		a = response.css('div.tbl div.cell::text').extract()
		page_n = a[0].split(" of ")
		print("Hello"+str(page_n[1]))
		i = i + 1
		# for i in range(int(page_n[1])+1):
		# 	print("Hello"+str(i))
		# 	pg_links.append("https://www.glassdoor.com/Job/bismarck-jobs-SRCH_IL.0,8_IC1156224_IP"+str(i)+".htm")
		# print(pg_links)
		if i <= int(page_n[1]):
			page_start = "https://www.glassdoor.com/Job/bismarck-jobs-SRCH_IL.0,8_IC1156224_IP"+str(i)+".htm"
			print("Hello"+str(i))
			yield scrapy.Request(page_start,callback=self.parse, dont_filter=True)
		


	def parse_attr(self, response):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		item = DmozItem()
		title = response.css('div.css-17x2pwl::text').extract()
		company_name = response.css('div.css-16nw49e::text').extract()
		
		try:	
			if company_name[0] == "N/A":
				company_name[0] = ""
		except IndexError:
			company_name = []
		location = response.css('div.css-1v5elnn::text').extract()
		salary = response.css('span.small::text').extract()
		data = response.css('span.css-sr4ps0::text').extract()
		try:
			job_type = data[0]
			if job_type == "N/A":
				job_type = ""
		except IndexError:
			job_type = ""
		try:
			industry = data[1]
			if industry == "N/A":
				industry = ""
		except IndexError:
			industry = ""
		try:
			company_size = data[2]
			if company_size == "N/A":
				company_sizem = ""
		except IndexError:
			company_size = ""
		job_function = response.css('span.css-o4d739::text').extract()
		if job_function == "N/A":
			job_function = ""
		data_img = response.css('img.lazy').xpath("@data-original").extract()
		apply_link = response.css('a.gd-ui-button').xpath("@href").extract() 	
		data = response.css('p::text').extract()

		try:
			apply_linkss  = 'https://www.glassdoor.com' + apply_link[0]
			responses = requests.get(apply_linkss, headers=headers)

			apply_links = responses.url
		except IndexError:
			apply_links = response.css('button.applyButton span::text').extract()
			apply_links = response.url
		try:
			img = data_img[1]
		except IndexError:
			img =""
		data_desc = ""
		for i in data:
			data_desc = data_desc + i +" "

		item['Title'] = title
		item['Company_name'] = company_name
		item['Location'] = location
		item['Salary'] = salary
		item['Job_type'] = job_type
		item['Industry'] = industry
		item['Company_size'] = company_size
		item['Job_function'] = job_function
		item['Img_Url'] = img
		item['apply_link'] = apply_links
		item['Description'] = data_desc
		return item
        
		