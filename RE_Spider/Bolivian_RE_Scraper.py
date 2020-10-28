### Bolivian_RE_Scraper.py
### Authors: DR
### Main file, calls all scrapers and transfers all data into Excel

import remax_scraper as REMAX
import c21_scraper as C21
import ultracasas_scraper as UC
import infocasas_scraper as IC
import data_cleaner
import xlsxwriter
from datetime import datetime
from datetime import date

# Transfer data to Excel
def Transfer_To_Excel(listings):
	# Open Excel Workbook and add a new Worksheet with today's data
	workbook = xlsxwriter.Workbook('Bolivian_Real_Estate_Data_' + str(date.today()) + '.xlsx')
	worksheet = workbook.add_worksheet('Data_' + str(date.today()))
	
	# Add a bold format to use to highlight cells.
	bold = workbook.add_format({'bold': True})

	# Write Header for Raw Data
	worksheet.write('A1', 'URL', bold)
	worksheet.write('B1', 'Type', bold)
	worksheet.write('C1', 'Price', bold)
	worksheet.write('D1', 'Dept', bold)
	worksheet.write('E1', 'Beds', bold)
	worksheet.write('F1', 'Baths', bold)
	worksheet.write('G1', 'Area (m^2)', bold)
	worksheet.write('H1', 'Lot Size (m^2)', bold)
	worksheet.write('I1', 'Year Built', bold)
	worksheet.write('J1', 'Agent', bold)
	worksheet.write('K1', 'Latitude', bold)
	worksheet.write('L1', 'Longitude', bold)
	worksheet.write('M1', 'Description', bold)
	#worksheet.write('L1', 'Amenities', bold)

	# Write Raw Data to sheet for current day
	row = 2
	for listing in listings:
		prop_type = data_cleaner.clean_type(listing.type)
		area = listing.area
		if listing.lot_size == listing.area and prop_type in ['Farm', 'Mine', 'Land']:
			area = "0"

		worksheet.write('A'+str(row), listing.url)
		worksheet.write('B'+str(row), data_cleaner.clean_type(listing.type))
		worksheet.write('C'+str(row), data_cleaner.clean_price(listing.price))
		worksheet.write('D'+str(row), data_cleaner.clean_dept(listing.dept))
		worksheet.write('E'+str(row), listing.beds)
		worksheet.write('F'+str(row), listing.baths)
		worksheet.write('G'+str(row), area)
		worksheet.write('H'+str(row), listing.lot_size)
		worksheet.write('I'+str(row), listing.year)
		worksheet.write('J'+str(row), listing.agent)
		worksheet.write('K' + str(row), listing.lat)
		worksheet.write('L' + str(row), listing.lon)
		worksheet.write('M'+str(row), listing.desc)
		#worksheet.write('L'+str(row), listing.amenities)
		row += 1

	worksheet.set_column(1, 1, 18)
	worksheet.set_column(2, 2, 14)
	worksheet.set_column(3, 3, 15)
	worksheet.set_column(4, 5, 6)
	worksheet.set_column(6, 7, 12)
	worksheet.set_column(8, 8, 8)
	worksheet.set_column(9, 9, 30)
	worksheet.set_column(10, 11, 16)

	workbook.close()


def Start_Site_Scraper(sitename):
	startTime = datetime.now()
	
	if sitename == 'remax':
		print("Scraping Remax...")
		Listings.extend(REMAX.Get_Remax_Data())
	elif sitename == 'c21':
		print("Scraping C21...")
		Listings.extend(C21.Get_C21_Data())
	elif sitename == 'ic':
		print("Scraping Infocasas...")
		Listings.extend(IC.Get_Infocasas_Data())
	elif sitename == 'uc':
		print("Scraping Ultracasas...")
		Listings.extend(UC.Get_Ultracasas_Data())
	else: 
		print ("Invalid website choice: " + str(sitename))
	
	print("Elements scraped:")
	print(str(len(Listings)))
	
	print("Time to complete:")
	print (datetime.now() - startTime)

if __name__ == "__main__":
	ogStartTime = datetime.now()
	Listings = []

	print("Web Crawler initialized at: " + str(ogStartTime))

	Start_Site_Scraper('uc')
	# Start_Site_Scraper('ic')
	Start_Site_Scraper('c21')
	Start_Site_Scraper('remax')

	Transfer_To_Excel(Listings)
	
	print("Program completed with elapsed time: ")
	print(datetime.now() - ogStartTime)
	
	print("Press Enter to exit program.")
	input()
