### infocasas_scraper.py 
### Authors: DR
### Scrapes listings from www.infocasas.com.bo

import Listing
import time
import math
from random import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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


def bypass_captcha(driver):
	driver.switch_to.default_content()
	print("Switch to new frame")
	iframes = driver.find_elements_by_tag_name("iframe")
	driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

	print("Wait for recaptcha-anchor")
	check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))

	print("Wait")
	time.sleep(random(1.67, 4.03))
	# self.wait_between(MIN_RAND, MAX_RAND)

	# action = ActionChains(driver);
	# human_like_mouse_move(action, check_box)

	print("Click")
	check_box.click()

	print("Wait")
	time.sleep(random(1.67, 4.03))
	# self.wait_between(MIN_RAND, MAX_RAND)

	# print("Mouse movements")
	# action = ActionChains(driver);
	# self.human_like_mouse_move(action, check_box)

	print("Switch Frame")
	driver.switch_to.default_content()
	iframes = driver.find_elements_by_tag_name("iframe")
	driver.switch_to.frame(iframes[2])

	print("Wait")
	time.sleep(random(5.81, 9.067))
	# self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

	print("Find solver button")
	capt_btn = WebDriverWait(driver, 50).until(
		EC.element_to_be_clickable((By.XPATH, '//button[@id="solver-button"]'))
	)

	print("Wait")
	time.sleep(random(5.81, 9.067))
	# self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

	print("Click")
	capt_btn.click()

	print("Wait")
	time.sleep(random(5.81, 9.067))
	# self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

	try:
		print("Alert exists")
		alert_handler = WebDriverWait(driver, 20).until(
			EC.alert_is_present()
		)
		alert = driver.switch_to.alert
		print("Wait before accept alert")
		time.sleep(random(1.67, 4.03))
		# self.wait_between(MIN_RAND, MAX_RAND)

		alert.accept()

		time.sleep(random(1.67, 4.03))
		# self.wait_between(MIN_RAND, MAX_RAND)
		print("Alert accepted, retry captcha solver")

		bypass_captcha(driver)
	except:
		print("No alert")

	print("Wait")
	driver.implicitly_wait(5)
	print("Switch")
	driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

	# try:
	# 	WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
	# 		(By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
	# 	WebDriverWait(browser, 10).until(
	# 		EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
	# except:
	# 	print("Couldn't bypass captcha")

	# try:
	# 	css_selector = "span[id^='recaptcha-anchor']"
	# 	captcha_checkbox = browser.find_element_by_css_selector(css_selector)
	# except NoSuchElementException:
	# 	print("No captcha found")
	# 	return
	# try:
	# 	captcha_checkbox.click()
	# except NoSuchElementException:
	# 	print("Couldn't click captcha.")


def setUpProfile(browser):
	browser.profile = webdriver.ChromeProfile()
	browser.profile.add_extension("buster_captcha_solver_for_humans-1.1.0.xpi")
	browser.profile.set_preference("security.fileuri.strict_origin_policy", False)  # disable Strict Origin Policy
	browser.profile.update_preferences()  # Update profile with new configs


def Get_Infocasas_Data():
	# New browser
	browser = webdriver.Chrome()
	setUpProfile(browser)
	# options = Options()
	# options.headless = True
	# options.add_argument("--window-size=1920,1200")
	# options.add_argument("--log-level=3")
	# browser = webdriver.Chrome(options=options)
	browser.set_page_load_timeout(-1)
	browser.set_script_timeout(5)

	# Go to URL
	browser.get(INFOCASAS_URL_HEAD + MIN_PRICE + INFOCASAS_URL_TAIL)
	time.sleep(SLEEP_TIME_SEARCH)
	bypass_captcha(browser)
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