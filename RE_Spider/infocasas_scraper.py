### infocasas_scraper.py 
### Authors: DR
### Scrapes listings from www.infocasas.com.bo

import Listing
import time
import math
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidSessionIdException

INFOCASAS_URL_HEAD = 'https://www.infocasas.com.bo/venta/casas-y-departamentos-y-lotes-o-terrenos-y-locales-comerciales-y-oficinas-y-quintas-o-campos-y-garaje-o-cocheras-y-negocio-especial-y-local-industrial-o-galpon-y-condominio-y-habitacion/desde-'
INFOCASAS_URL_TAIL = '/dolares'
MIN_PRICE = '300000'
SLEEP_TIME_SEARCH = 8
SLEEP_TIME_LISTING = 3


def Extract_Data(browser):
	try: 
		url = browser.current_url
	except WebDriverException:
		print("Entry skipped due to WDE")
		url = ""
		return -1

	try:
		prop_type = browser.find_element_by_xpath("//div[@class='dot home']/div[@class='dotInfo']").text
	except NoSuchElementException or AttributeError:
		prop_type = ""

	try:
		price = clean_price(browser.find_element_by_xpath("//p[@class='precio-final']").text, ',')
	except NoSuchElementException or AttributeError:
		price = ""

	try:
		desc = browser.find_element_by_xpath("/html/body/div/div/div/h1").text
	except NoSuchElementException or AttributeError:
		desc = ""

	try:
		dept = browser.find_element_by_xpath("/html/body/div/div/div/a[4]").text
	except NoSuchElementException or AttributeError:
		dept = ""

	try:
		bathrooms = clean_rooms(browser.find_element_by_xpath("//div[@class='dot shower']/div[@class='dotInfo']").text)
	except NoSuchElementException or AttributeError:
		bathrooms = ""

	try:
		bedrooms = clean_rooms(browser.find_element_by_xpath("//div[@class='dot bed']/div[@class='dotInfo']").text)
	except NoSuchElementException or AttributeError:
		bedrooms = ""

	try:
		built_area = clean_area(browser.find_element_by_xpath("//div[@class='dot m2']/div[@class='dotInfo']").text, ',')
	except NoSuchElementException or AttributeError:
		built_area = ""

	try:
		lot_size = clean_area(browser.find_element_by_xpath("//div[@class='dot tree']/div[@class='dotInfo']").text, ',')
	except NoSuchElementException or AttributeError:
		lot_size = ""

	try:
		year = clean_year(browser.find_element_by_xpath(("//div[preceding-sibling::p[contains(text(),'Año de construcción')]]")).text)
	except NoSuchElementException or AttributeError:
		year = ""

	try:
		agent = browser.find_element_by_xpath("//p[@class='titulo-inmobiliaria']").text
	except NoSuchElementException or AttributeError:
		agent = ""

	return Listing.Listing(url, prop_type, price, desc, bathrooms, bedrooms, built_area, lot_size, year, dept, agent)
	

def clean_rooms(value):
	try:
		return value.split()[0]
	except IndexError:
		return value


def clean_price(value, delim):
	if delim in value:
		value = value.split(delim)[0]
	numeric_filter = filter(str.isdigit, value)
	return ("".join(numeric_filter))


def clean_area(value, delim):
	if delim in value:
		value = value.split(delim)[0]
	numeric_filter = filter(str.isdigit, value)
	return ("".join(numeric_filter))[:-1]


def clean_year(year):
	if '/' in year:
		year = year.split('/')[0]
	if ' ' in year:
		year = year.split()[0]
	numeric_filter = filter(str.isdigit, year)
	return ("".join(numeric_filter))


def Get_Infocasas_Data():
	# New browser
	#browser = webdriver.Firefox()
	browser = webdriver.Chrome()
	browser.set_page_load_timeout(-1)
	browser.set_script_timeout(5)

	# Go to URL
	browser.get(INFOCASAS_URL_HEAD + MIN_PRICE + INFOCASAS_URL_TAIL)
	time.sleep(SLEEP_TIME_SEARCH)
	
	# Figure out how many pages to flip through
	IC_listings = []
	IC_urls_clean = []

	# Scrape items from each page
	page_num = 1
	while(len(browser.find_elements_by_xpath("//a[@class='next ']")) > 0):# and page_num < 2): #**UNCOMMENT THIS FOR TEST PURPOSES**
		# Get all the listings' URLs
		IC_urls_dirty = browser.find_elements_by_xpath("/html/body/div/div/div/div/div/div/div/div/div/a[@href]")
		for url_element in IC_urls_dirty:
			url = url_element.get_attribute("href")
			# Make sure it's a valid URL
			if url.startswith("https://www.infocasas"):
				IC_urls_clean.append(url)

		# Go to next page
		browser.find_element_by_xpath("//a[@class='next ']").click()
		page_num += 1
		time.sleep(SLEEP_TIME_SEARCH)

	# Extract data from each of the cleaned URLs		
	for url in IC_urls_clean:
		try:
			browser.get(url)
			time.sleep(SLEEP_TIME_LISTING)
			prop = Extract_Data(browser)
			if prop != -1:
				IC_listings.append(prop)
		except (TimeoutException, InvalidSessionIdException):
			continue

	browser.quit()
	return IC_listings


# Get_Infocasas_Data()