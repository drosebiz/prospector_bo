# This file contains functions that will generate and return plots according to user input
import pandas as pd
import GatherData as gd
import numpy as np
import plotly.graph_objects as go


def Scatter(data, x, y,
            title="", template="none",
            filterType="Any",
            sizeMarkers="Off", markerSizer="LotSize",
            colorSeries="On", colorCoder="Type",
            minPrice=0, maxPrice=100000000,
            numBeds=0, numBaths=0):

    # Sort along x-axis
    data = data.sort_values(by=x, na_position='first')
    traces = []
    seriesList = ['']
    if colorSeries == "On":
        seriesList = data[colorCoder].unique()
    # Fill in default values for NaN
    values = {
        'Price': 0, 'LotSize': 0, 'Area': 0, 'Beds': 0, 'Baths': 0, 'YearBuilt': 0,
        'Type': 'Not Specified', 'Description': '', 'Dept': 'Not Specified', 'Agent': 'None Listed',
        'URL': 'https://www.prospector.com/', 'Website': ''
    }
    data = data.fillna(value=values)

    # Filter Data
    if isinstance(minPrice, int):
        data = data[(data.Price >= minPrice)]
    if isinstance(maxPrice, int):
        data = data[(data.Price <= maxPrice)]
    if len(filterType) > 0:
        data = data.query('Type in' + str(filterType))
    if numBeds > 0:
        data = data[(data.Beds >= numBeds)]
    if numBaths > 0:
        data = data[(data.Baths >= numBaths)]

    # Generate trace(s)
    for series in seriesList:
        # Get series-specific data, if we're color coding
        if colorSeries == "On":
            dfNew = data[(data[colorCoder] == series)]
        else:
            dfNew = data

        if sizeMarkers == "On":
            maxSizerVal = max(data[markerSizer].values.tolist())
            sizeList = dfNew[markerSizer].values.tolist()
            marker_style = dict(
                size=sizeList,
                sizemode='area',
                sizeref=(2 * maxSizerVal / (50**2)),
                sizemin=10,
            )
        else:
            marker_style = dict(size=10)

        customdata = np.stack((dfNew['URL'], dfNew['Price'], dfNew['Beds'], dfNew['Baths'],
                               dfNew['LotSize'], dfNew['Area'], dfNew['YearBuilt']), axis=-1)
        newTrace = go.Scatter(
            name=series,
            x=dfNew[x],
            y=dfNew[y],
            mode='markers',
            marker=marker_style,
            # text=text,
            visible=True,
            customdata=customdata,
            hovertemplate="Site: " + dfNew['Website'] +
                          "<br>Department: " + dfNew['Dept'] +
                          "<br>Price: $%{customdata[1]: .2f}" +
                          "<br>Bedrooms: %{customdata[2]}" +
                          "<br>Bathrooms: %{customdata[3]}" +
                          "<br>Lot Size: %{customdata[4]}" + "m²" +
                          "<br>Area: %{customdata[5]}" + "m²" +
                          "<br>Year Built: %{customdata[6]}" +
                          "<br>Agent: " + dfNew['Agent'] +
                          "<extra></extra>",
        )
        traces.append(newTrace)

    fig = go.Figure(data=traces)
    fig.update_layout(
        template=template,
        title=dict(text=title),
        hovermode='x',
    )
    format_xaxis(fig, x)
    format_yaxis(fig, y)
    return fig


def Bar(data, x, y,
        title="", template="none"):

    traces = []
    y_values = []
    if y in ['PricePerSqMeterInterior', 'PricePerSqMeterExterior']:
        for category in data[x].unique():
            # print(category)
            dfNew = data[(data[x] == category)]
            y_values.append(dfNew[y].mean(skipna=True))
    else:
        y_values = data[y]
    # print(y_values)
    print(data[data.Dept == 'San Javier'].LotSize)
    newTrace = go.Bar(
        x=data[x],
        y=y_values,
    )
    traces.append(newTrace)
    fig = go.Figure(data=traces)
    fig.update_layout(
        template=template,
        title=dict(text=title),
        # hovermode='x',
    )
    format_xaxis(fig, x)
    format_yaxis(fig, y)
    return fig


def format_xaxis(fig, attr):
    if attr == 'Price':
        fig.update_xaxes(
            tickprefix="$",
            title_text='Price ($USD)'
        )
    if attr in ["LotSize", "Lot Size"]:
        fig.update_xaxes(
            title_text='Lot Size (m²)'
        )
    if attr == 'Area':
        fig.update_xaxes(
            title_text='Interior Area (m²)'
        )
    if attr == 'Beds':
        fig.update_xaxes(
            title_text='# Bedrooms'
        )
    if attr == 'Baths':
        fig.update_xaxes(
            title_text='# Bathrooms'
        )
    if attr == 'Year':
        fig.update_xaxes(
            title_text='Year Built'
        )
    # return fig


def format_yaxis(fig, attr):
    if attr == 'Price':
        fig.update_yaxes(
            tickprefix="$",
            title_text='Price ($USD)'
        )
    if attr in ["LotSize", "Lot Size"]:
        fig.update_yaxes(
            title_text='Lot Size (m²)'
        )
    if attr == 'Area':
        fig.update_yaxes(
            title_text='Interior Area (m²)'
        )
    if attr == 'Beds':
        fig.update_yaxes(
            title_text='# Bedrooms'
        )
    if attr == 'Baths':
        fig.update_yaxes(
            title_text='# Bathrooms'
        )
    if attr == 'Year':
        fig.update_yaxes(
            title_text='Year Built'
        )
    # return fig

