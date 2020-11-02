import Listing
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import InvalidSessionIdException

ULTRACASAS_URL = 'https://ultracasas.com'
# MIN_PRICE must have comma and choose from the following choices:
# 0, 50k, 100k, 200k, 300k, 400k, 500k, 600k
MIN_PRICE = '300,000'
SLEEP_TIME_SEARCH = 5
SLEEP_TIME_LISTING = 2


def Search_Ultracasas(browser):
    # click 'No gracias' for notifications
    # no_gracias_button = browser.find_element_by_xpath("//button[@id ='onesignal-popover-cancel-button']")
    # no_gracias_button.click()

    # from home page, click search
    browser.find_element_by_xpath("//div/span/button[@class='btn btn-info btn-lg']").click()
    time.sleep(SLEEP_TIME_SEARCH)

    # click checkboxes so the page regenerates
    buttons = browser.find_elements_by_xpath(
        "//html/body/div[1]/section[2]/div/div/div[1]/aside[1]/div[2]/form/div[2]/div/label[@class ='checkbox-inline "
        "no-padding']")
    for btn in buttons[1:]:
        btn.click()

    time.sleep(SLEEP_TIME_LISTING)

    # Set min price
    price_select = Select(browser.find_element_by_xpath("//select[@id='min']"))
    price_select.select_by_value(MIN_PRICE)
    time.sleep(SLEEP_TIME_SEARCH)


def Extract_Data(browser):
    bathrooms = ""
    bedrooms = ""

    try:
        url = browser.current_url
    except WebDriverException:
        print("Entry skipped due to WDE")
        return -1

    try:
        prop_type = browser.find_element_by_xpath("//span[@class='forsale']").text
        # Apts and other complexes have a directory listing which doesn't provide us information.
        # We can tell it's a directory when the price says "en venta desde".
        # Ignore these listings and move on.
        if prop_type.lower().strip() == 'en venta desde':
            return -1
        else:
            # Change "Casa en venta" to "casa"
            prop_type = prop_type.lower().split(' en venta')[0]  # have to cut off the 'en venta' in 'casa en venta'
    except (NoSuchElementException, AttributeError):
        prop_type = ""

    try:
        price_dirty = browser.find_element_by_xpath("//p[@class='numeros']").text
        price = clean_price(price_dirty)
    except (NoSuchElementException, AttributeError):
        price = ""

    try:
        desc = browser.find_element_by_xpath("//h1[@itemprop='streetAddress']").text
    except (NoSuchElementException, AttributeError):
        desc = ""

    try:
        dept = clean_dept(browser.find_element_by_xpath("//div[@class='titular']/h2").text)
    except (NoSuchElementException, AttributeError):
        dept = ""

    try:
        br_bath = browser.find_element_by_xpath("//div[@class='titular']/h3").text
        for data in br_bath.split('·'):
            if "Dormitorios" in data:
                bedrooms = int(data.split()[0])
            elif "baños" in data:
                bathrooms = float(data.split()[0])
    except (NoSuchElementException, AttributeError):
        bedrooms = ""
        bathrooms = ""

    try:
        xpath = "//div[contains(@class,'listado-features-texto')]/h4[contains(text(), " \
                "'Construido')]/following-sibling::p "
        built_area = clean_area(browser.find_element_by_xpath(xpath).text.split(' ')[0], '.')
    except (NoSuchElementException, AttributeError):
        built_area = ""

    try:
        xpath = "//div[contains(@class,'listado-features-texto')]/h4[contains(text(), 'Terreno')]/following-sibling::p"
        lot_size = clean_area(browser.find_element_by_xpath(xpath).text.split(' ')[0], '.')
    except (NoSuchElementException, AttributeError):
        lot_size = ""

    try:
        dirty = browser.find_element_by_xpath("//p[preceding-sibling::h4[contains(text(),'Año construcción')]]").text
        year = clean_year(dirty)
    except (NoSuchElementException, AttributeError):
        year = ""

    try:
        agent = browser.find_element_by_xpath("//p[@class='name-agent-contact nombre']/a").text
    except (NoSuchElementException, AttributeError):
        agent = ""

    try:
        css_selector = "img[class^='width-100-percent a-btn-style']"
        location = browser.find_element_by_css_selector(css_selector).get_attribute('onclick')
        coords = location.split('(')[1].split(')')[0].split(',')
        lat = float(coords[0])
        lon = float(coords[1])
    except (NoSuchElementException, AttributeError):
        lat = ""
        lon = ""

    # Create new Listing object w clean data
    return Listing.Listing(url, prop_type, price, desc, bathrooms, bedrooms, built_area,
                           lot_size, year, dept, agent, lat, lon)


def clean_price(value):
    numeric_filter = filter(str.isdigit, value)
    return "".join(numeric_filter)


def clean_area(value, delim):
    value = value.split()[0]
    if delim in value:
        value = value.split(delim)[0]
    numeric_filter = filter(str.isdigit, value)
    try:
        return int("".join(numeric_filter))
    except ValueError:
        return ''


def clean_dept(dept):
    if ',' in dept:
        split_dept = dept.split(',')
        dept = split_dept[-1]
        if dept[0] == " ":
            dept = dept[1:]
    return dept


def clean_year(year):
    if '/' in year:
        year = year.split('/')[0]
    if ' ' in year:
        year = year.split()[0]
    currentYear = datetime.datetime.now().year
    numeric_filter = filter(str.isdigit, year)
    year = int("".join(numeric_filter))
    if year < 1000:
        year = currentYear - year
    return year


def Get_Ultracasas_Data():
    # New browser
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(-1)
    browser.set_script_timeout(4)

    # Go to URL
    browser.get(ULTRACASAS_URL)
    time.sleep(SLEEP_TIME_SEARCH)
    Search_Ultracasas(browser)

    # Figure out how many pages to flip through
    UC_listings = []
    UC_urls_clean = []
    page_num = 1

    # Scrape items from each page
    # FOR TEST: uncomment this while statement, comment out the following while statement
    # while len(browser.find_elements_by_xpath("//a[@id='linkNext']")) > 0 and page_num < 3:
    while len(browser.find_elements_by_xpath("//a[@id='linkNext']")) > 0:
        # Get all the listings' URLs
        UC_urls_dirty = browser.find_elements_by_xpath("//div[@class='inmuebles-item-titular-tit']/a")
        for url_element in UC_urls_dirty:
            url = url_element.get_attribute("href")
            UC_urls_clean.append(url)

        # Go to next page
        page_num += 1
        browser.find_element_by_xpath("//a[@id='linkNext']").click()
        time.sleep(SLEEP_TIME_SEARCH)

    # Extract data from each of the cleaned URLs
    for url in UC_urls_clean:
        try:
            browser.get(url)
            time.sleep(SLEEP_TIME_LISTING)
            prop = Extract_Data(browser)
            if prop != -1:
                UC_listings.append(prop)
        except (TimeoutException, InvalidSessionIdException):
            continue

    browser.quit()
    return UC_listings
