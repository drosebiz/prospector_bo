# Listing.py
# Authors: DR
# Definition for Listing object created from each property's data
# import googlemaps as maps
# from geopy.geocoders import Nominatim

class Listing:
    def __init__(self, url, prop_type, price="Unlisted", desc="", baths="", beds="", area="", lot_size="",
                 year="Unlisted", dept="", agent="", lat="", lon=""):
        self.url = url
        self.type = prop_type
        self.price = price
        self.baths = baths
        self.beds = beds
        self.area = area
        self.desc = desc
        self.lot_size = lot_size
        self.year = year
        self.dept = dept
        self.agent = agent
        self.lat = lat
        self.lon = lon


# la = '-17.736306'
# lo = '-63.169639'
# geolocator = Nominatim(user_agent="pros")
# location = geolocator.reverse(la + ',' + ' ' + lo)
# print (location.address)
