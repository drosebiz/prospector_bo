import pandas as pd
import re
# import pandarallel
import dask
from scipy import stats
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.callbacks import Points, InputDeviceState
from ipywidgets import widgets, Output, VBox
import webbrowser

# Derives the website name ('remax', 'c21', etc.) from the full URL
def getSiteFromURL(url):
    if "https://www." in url or "http://www." in url:
        # get the indices of both "."s, after www and before com
        firstDot = url.find('.')
        secondDot = url[firstDot + 1:].find('.') + firstDot
        # return the substring in between
        url = url[firstDot + 1:secondDot + 1]
    else:
        # get the indices of the end of https:// and beginning of .com (or .bo, or whatever)
        secondSlash = url.find('/') + 1  # add 1 because there are two slashes
        firstDot = url.find('.')
        # return the substring in between
        url = url[secondSlash + 1:firstDot]
    return url


# Filtering functions for DataFrames
def getPriceRange(data, min=0, max=1000000000):
    df = data[(data.Price >= min) & (data.Price <= max)]
    return df


def getLotSizeRange(data, min=0, max=10000000):
    df = data[(data.LotSize >= min) & (data.LotSize <= max)]
    return df


def getAreaRange(data, min=0, max=10000000):
    df = data[(data.Area >= min) & (data.Area <= max)]
    return df


def getBedsRange(data, min=0, max=100000):
    df = data[(data.Beds >= min) & (data.Beds <= max)]
    return df


def getBathsRange(data, min=0, max=100000):
    df = data[(data.Baths >= min) & (data.Baths <= max)]
    return df


def getYearRange(data, min=0, max=2020):
    df = data[(data.YearBuilt >= min) & (data.YearBuilt <= max)]
    return df


def getPropType(data, propType):
    df = data[(data.Type == propType)]
    return df


def getWebsite(data, site):
    return data[(data.Website == site)]


def gatherData(path, name):
    # Read file
    data = pd.read_excel(path + name)

    # Rename columns so there are no spaces
    data = data.rename(columns={
        "Lot Size (m^2)": "LotSize",
        "Area (m^2)": "Area",
        "Year Built": "YearBuilt"
    })

    # Create New Columns
    data['Website'] = data['URL'].apply(lambda x: getSiteFromURL(x))
    data['PricePerSqMeterInterior'] = data['Price'] / data['Area']
    data['PricePerSqMeterExterior'] = data['Price'] / data['LotSize']

    return data

    # # Create DataFrame from our data
    # df = pd.DataFrame(data,
    #                   columns=['Price', 'LotSize', 'Area', 'Beds', 'Baths', 'YearBuilt', 'Type', 'Description', 'URL',
    #                            'Website'])
    # # df = df.dropna()
    #
    # # df = getPropTypes(df, ['Casa', "Condo/Apartment"])
    # df = getPropType(df, 'Casa')
    # df = getPriceRange(df, 350000, 1200000)
    # df = getLotSizeRange(df, max=500)
    # # df = getAreaRange(df, min=250, max=650)
    # # df = getBedsRange(df, 1, 8)
    # # df = getBathsRange(df, 1, 8)
    # # df = getYearRange(df, 1950)
    # df.Type.unique()
