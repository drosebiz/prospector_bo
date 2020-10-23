### c21_scraper.py 
### Authors: DR
### Scrapes listings from www.c21.com.bo

import Listing
import time
import math
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidSessionIdException

C21_URL_HEAD = 'https://c21.com.bo/busqueda/tipo_casa-o-casa-en-condominio-o-departamento-o-deposito-o-edificio-o-hotel-o-local-o-oficinas-o-penthouse-o-proyecto-o-quinta-o-rural-o-terreno-o-tinglado/operacion_venta/precio-desde_'
C21_URL_MID = '/moneda_usd/'
C21_RES_PER_PAGE = 9
MIN_PRICE = '300000'
SLEEP_TIME_SEARCH = 3  # 8
SLEEP_TIME_LISTING = 1  # 3

def Extract_Data(browser):
	try:
		url = browser.current_url
	except WebDriverException:
		print("Entry skipped due to WDE")
		url = ""
		return -1
	try:
		prop_type = browser.find_element_by_xpath("//span[preceding-sibling::i[1][contains(@class,'fa-tags')]]").text
	except NoSuchElementException or AttributeError:
		prop_type = ""

	try:
		price = clean_price_and_area(browser.find_element_by_xpath("//span[preceding-sibling::i[1][contains(@class,'fa-money')]]").text, ',')
	except NoSuchElementException or AttributeError:
		price = ""

	try:
		desc_items = browser.find_elements_by_xpath("//html/body/main/div/div/div/span")
		desc = desc_items[0].text
		for item in desc_items[1:]:
			desc = desc + ", " + item.text
		desc = desc[:-2]
		dept = clean_desc(desc)
	except NoSuchElementException or AttributeError:
		desc = ""
		dept = ""

	try:
		bathrooms = browser.find_element_by_xpath("//span[preceding-sibling::i[1][contains(@class,'fa-bath')]]").text
	except NoSuchElementException or AttributeError:
		bathrooms = ""

	try:
		bedrooms = browser.find_element_by_xpath("//span[preceding-sibling::i[1][contains(@class,'fa-bed')]]").text
	except NoSuchElementException or AttributeError:
		bedrooms = ""

	try:
		built_area = clean_price_and_area(browser.find_element_by_xpath("//span[preceding-sibling::i[1][contains(@class,'fa-ruler-triangle')]]").text, ',')
	except NoSuchElementException or AttributeError:
		built_area = ""

	try:
		lot_size = clean_price_and_area(browser.find_element_by_xpath("//span[preceding-sibling::i[1][contains(@class,'fa-expand')]]").text, ',')
	except NoSuchElementException or AttributeError:
		lot_size = ""

	try:
		year = clean_year(browser.find_element_by_xpath("//span[preceding-sibling::i[1][contains(@class,'fa-clock')]]").text)
	except NoSuchElementException or AttributeError:
		year = ""

	try:
		agent_first = browser.find_element_by_xpath("/html/body/main/div[7]/div[1]/div[1]").text
		agent_last = browser.find_element_by_xpath("/html/body/main/div[7]/div[1]/span[1]").text
		agent = agent_first + " " + agent_last
	except NoSuchElementException or AttributeError:
		agent = ""

	return Listing.Listing(url, prop_type, price, desc, bathrooms, bedrooms, built_area, lot_size, year, dept, agent)


def clean_price_and_area(value, delim):
	if delim in value:
		value = value.split(delim)[0]
	numeric_filter = filter(str.isdigit, value)
	return ("".join(numeric_filter))


def clean_year(year):
	if '/' in year:
		year = year.split('/')[0]
	if ' ' in year:
		year = year.split()[0]
	currentYear = datetime.datetime.now().year
	numeric_filter = filter(str.isdigit, year)
	year = int("".join(numeric_filter))
	if year < 1000:
		year = currentYear - int(year)
	return str(year)


def clean_desc(desc):
	if ',' in desc:
		split_desc = desc.split(',')
		desc = split_desc[-1]
		if desc[0] == " ":
			desc = desc[1:]
	return desc


def Get_C21_Page_Num(browser):
	num_results_dirty = browser.find_element_by_xpath("//span[contains(text(),'1-9 de')]").text
	num_results_clean = num_results_dirty.split()[-1]
	numeric_filter = filter(str.isdigit, num_results_clean)
	return math.ceil(int("".join(numeric_filter)) / C21_RES_PER_PAGE)


def Load_Next_C21_Page(browser, page):
	browser.get(C21_URL_HEAD + MIN_PRICE + C21_URL_MID+ '/pagina_' + str(page))
	time.sleep(SLEEP_TIME_SEARCH)

def Get_C21_Data():#browser):
	# New browser
	#browser = webdriver.Firefox()
	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1200")
	options.add_argument("--log-level=3")
	browser = webdriver.Chrome(options=options)
	browser.set_page_load_timeout(20)
	browser.set_script_timeout(5)

	# Go to URL
	browser.get(C21_URL_HEAD + MIN_PRICE + C21_URL_MID)
	time.sleep(SLEEP_TIME_SEARCH)
	
	# Figure out how many pages to flip through
	num_pages = Get_C21_Page_Num(browser)
	# FOR TEST PURPOSES, UNCOMMENT NEXT LINE
	# num_pages = 5
	c21_listings = []
	c21_urls_clean = []

	#print (str(num_pages) + " C21 pages to scrape.")

	# Scrape items from each page
	for page_num in range(1, num_pages+1):
		# Get next page and find all gallery items
		Load_Next_C21_Page(browser, page_num)
		#c21_items_page = browser.find_elements_by_xpath("//*[@class='gallery-item-container']")
		c21_items_page = browser.find_elements_by_xpath("//div/div/div/div/div[@class ='card rounded-0']")


		# Get all the listings' URLs
		c21_urls_dirty = browser.find_elements_by_xpath("/html/body/main/div/div/div/div/div/a[@href]")
		for url_element in c21_urls_dirty:
			url = url_element.get_attribute("href")
			if "/propiedad/" in url and url not in c21_urls_clean:
				c21_urls_clean.append(url)

		# if no properties on screen, break out of loop
		if len(c21_items_page) == 0:
			break

	# Extract data from each of the cleaned URLs		
	for url in c21_urls_clean:
		try:
			browser.get(url)
			time.sleep(SLEEP_TIME_LISTING)
			prop = Extract_Data(browser)
			if prop != -1:
				c21_listings.append(prop)
		except (TimeoutException, InvalidSessionIdException):
			continue

	browser.quit()
	return c21_listings

