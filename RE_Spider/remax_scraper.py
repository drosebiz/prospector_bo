# remax_scraper.py
# Authors: DR
# Scrapes listings from www.remax.bo

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

REMAX_URL_HEAD = 'http://www.remax.bo/publiclistinglist.aspx#mode=gallery&tt=261&min='
REMAX_URL_MID = '&cur=USD&sb=PriceDecreasing&page='
REMAX_URL_TAIL = '&sc=120&sid=e1083e16-9f2d-4c67-bab4-45bdb9ec1b0a'
MIN_PRICE = '300000'
REMAX_RES_PER_PAGE = 24
SLEEP_TIME_SEARCH = 4
SLEEP_TIME_LISTING = 2


# Extract data from the individual listing URL
def Extract_Data(browser):
    try:
        url = browser.current_url
    except WebDriverException:
        print("Entry skipped due to WDE")
        return -1

    # Get 'dirty' data straight from page then clean it, if element exists
    try:
        dirty_info = browser.find_elements_by_xpath("//div[@class='data-item-label']")
    except NoSuchElementException or AttributeError:
        dirty_info = ""

    bedrooms = ""
    bathrooms = ""
    lot_size = ""
    built_area = ""
    year = ""

    for data in dirty_info:
        attribute_whole = data.get_attribute('data-original-title')
        qty = attribute_whole.split()[-1]
        if "Bedrooms" in attribute_whole:
            bedrooms = int(qty)
        elif "Bathrooms" in attribute_whole:
            bathrooms = float(qty)
        elif "Lot Size (m2)" in attribute_whole:
            lot_size = clean_price_and_area(qty, '.')
        elif "Lot Size" in attribute_whole:
            lot_size = clean_price_and_area(qty, '.')
        elif "Built Area" in attribute_whole:
            built_area = clean_price_and_area(qty, '.')
        elif "Year" in attribute_whole:
            try:
                year = clean_year(qty)
            except ValueError:
                year = ''

    try:
        price_dirty = browser.find_element_by_xpath("//a[@itemprop='price']")
        price = clean_price_and_area(price_dirty.get_attribute("content"), '.')
    except NoSuchElementException or AttributeError:
        price = ""

    try:
        css_selector = "div[class^='col-xs-12 key-title'] h1"
        prop_type = browser.find_element_by_css_selector(css_selector).text.split('-')[0].strip()
    except NoSuchElementException or AttributeError:
        prop_type = ""

    try:
        desc = browser.find_element_by_css_selector("div[class^='col-xs-12 key-address']").text
        dept = clean_desc(desc)
    except NoSuchElementException or AttributeError:
        desc = ""
        dept = ""

    try:
        agent = browser.find_element_by_xpath("//h3/a/span[@itemprop='name']").text
    except NoSuchElementException or AttributeError:
        agent = ""

    try:
        css_selector = "div.gallery-map-map div[class^='googlemap-office'] script[type^='text/javascript']"
        location = browser.find_element_by_css_selector(css_selector)
        innerhtml = location.get_property('innerHTML')
        coords = clean_coords(innerhtml)
        lat = float(coords['lat'])
        lon = float(coords['lon'])

    except NoSuchElementException or AttributeError:
        lat = ""
        lon = ""

    # Create new Listing object w clean data
    return Listing.Listing(url, prop_type, price, desc, bathrooms, bedrooms, built_area,
                           lot_size, year, dept, agent, lat, lon)


def clean_price_and_area(value, delim):
    if delim in value:
        value = value.split(delim)[0]
    numeric_filter = filter(str.isdigit, value)
    try:
        return int("".join(numeric_filter))
    except ValueError:
        return ''


def clean_desc(desc):
    if ',' in desc:
        split_desc = desc.split(',')
        desc = split_desc[-1]
        if desc[0] == " ":
            desc = desc[1:]
    return desc


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
    return year


def clean_coords(html):
    lat = html.split('var lat = ')[1].split(';')[0]
    lng = html.split('var lng = ')[1].split(';')[0]
    return dict(
        lat=lat,
        lon=lng
    )


def Get_Remax_Page_Num(browser):
    num_results_txt = browser.find_element_by_xpath("//span[contains(text(),'Matches')]").text
    numeric_filter = filter(str.isdigit, num_results_txt)
    return math.ceil(int("".join(numeric_filter)) / REMAX_RES_PER_PAGE)


def Load_Next_Remax_Page(browser, page):
    browser.get(REMAX_URL_HEAD + MIN_PRICE + REMAX_URL_MID + str(page) + REMAX_URL_TAIL)
    time.sleep(SLEEP_TIME_SEARCH)


def Get_Remax_Data():  # browser):
    # New browser
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(20)
    browser.set_script_timeout(5)

    # Go to URL
    browser.get(REMAX_URL_HEAD + MIN_PRICE + REMAX_URL_MID + str(1) + REMAX_URL_TAIL)
    time.sleep(SLEEP_TIME_SEARCH)

    # Figure out how many pages to flip through
    num_pages = Get_Remax_Page_Num(browser)
    # FOR TEST PURPOSES, UNCOMMENT NEXT LINE
    # num_pages = 3
    remax_listings = []
    remax_urls_clean = []

    # Scrape items from each page
    for page_num in range(1, num_pages + 1):
        # Get next page and find all gallery items
        Load_Next_Remax_Page(browser, page_num)
        remax_items_page = browser.find_elements_by_xpath("//*[@class='gallery-item-container']")

        # Get all the listings' URLs
        remax_urls_dirty = browser.find_elements_by_xpath(
            "/html/body/div/form/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a[@href]")
        for url_element in remax_urls_dirty:
            url = url_element.get_attribute("href")
            if "/en/listings/" in url and url not in remax_urls_clean:
                remax_urls_clean.append(url)

        # if no properties on screen, break out of loop
        if len(remax_items_page) == 0:
            break

    # Extract data from each of the cleaned URLs
    for url in remax_urls_clean:
        try:
            browser.get(url)
            time.sleep(SLEEP_TIME_LISTING)
            prop = Extract_Data(browser)
            if prop != -1:
                remax_listings.append(prop)
        except (TimeoutException, InvalidSessionIdException):
            continue

    browser.quit()
    return remax_listings
