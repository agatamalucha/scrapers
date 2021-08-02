import scrapy
from pathlib import Path
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import csv
from random import randrange
from datetime import datetime
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from datetime import date
from houses.items import HousesItem

## AVOID HANDSHAKE ERRORS
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--incognito")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")


software_names = [SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value,] 
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

today = date.today()
todays_date = today.strftime("%Y-%m-%d")

urls = []


class HousesSpiderSpider(scrapy.Spider):
	name = 'houses_spider'
	allowed_domains = ['homes.mitula.ie/houses-ballincollig']
	start_urls = ['https://homes.mitula.ie/houses-ballincollig/']

	def parse(self, response):
		print(str(Path(Path.cwd(), "chromedriver.exe")))
		self.driver = webdriver.Chrome(str(Path(Path.cwd(), "chromedriver.exe")), chrome_options=options)
		self.driver.set_window_size(randrange(1100, 1200), randrange(800, 900))


		for page in range(1,16):
			print(page)
			sleep(1)		
			self.driver.get(f"https://homes.mitula.ie/houses-ballincollig/{page}")


			sel = Selector(text=self.driver.page_source)
			adverts = sel.xpath('//div[contains(@class, "item-card__information  ")]')
			print(len(adverts))
			
			for ad in adverts:

						  
				price = ad.xpath('.//div[contains(@class, "item-card__price ")]/text()').extract_first()
				address = ad.xpath('.//span[contains(@class, "item-card__title ")]/text()').extract_first()
				rooms =  ad.xpath('.//div[contains(@class, "item-card__property")]/span/text()').extract_first()

				l=ItemLoader(item=HousesItem(),selector= ad)

				l.add_value('price',price)
				l.add_value('address',address)
				l.add_value('rooms',rooms)
				yield l.load_item()


		# self.driver.quit()




			








# address = response.xpath('//*[@itemprop="name"]/@content').extract_first()
# price = response.xpath('//*[@class="item-card__price "]').extract_first()
# rooms =  response.xpath('//*[@itemprop="numberOfRooms"]/@content').extract_first()
