import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import webbrowser
import GeneratePlot as gen
import GatherData as gd
import plotly.graph_objects as go

# Important User Variables
file_path = ""  # "\\Users\\DRose\\Documents\\Mexico_Demo\\"
file_name = "Bolivian_Real_Estate_Data_2020-08-31.xlsx"

# Plotly Settings
pd.options.plotting.backend = 'plotly'

# Dash Styling
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__, external_style_sheets=[dbc.themes.CYBORG])
app = dash.Dash(__name__)
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        # 'overflowX': 'scroll'
    }
}
colors = {
    'background': '#111111',  # plotly black
    'tabs': '#808080',  # Silver
    'tabBorder': '#D4AF37',  # Gold
    'tabSelectedBorder': '#808080',  # Silver
    'tabSelected': '#D4AF37',  # Gold
    'tabText': '#D4AF37',  # Gold
    'tabSelectedText': '#808080',  # Silver
    'title': '#D4AF37',  # Gold
    'headerBorder': '#808080',  # Silver
    'text': '#FFF8DC',  # Cornsilk
    'dropdown': '#F8DDA8',  # Goldenrod
    'dropdownSelectText': '#FFF8DC',  # Cornsilk
    'dropdownText': '#111111',  # plotly black
    'dropdownBorder': '#FFF8DC',  # Cornsilk
}
fonts = {
    'header': ['Palatino Linotype', 'Book Antiqua', 'Palatino', 'serif'],
    'tabs': ['Palatino Linotype', 'Book Antiqua', 'Palatino', 'serif'],
    'other': ['Lucida Sans Unicode', 'Lucida Grande', 'sans-serif'],
}

theme_dropdown_style= {
    'textAlign': 'left',
    # 'background': colors['dropdown'],
    # 'color': colors['dropdownText'],
    'font-family': fonts['other'],
    'font-size': '15px',
    # 'border': '1px solid ' + colors['dropdownBorder'],
    'width': '150px',
    'display': 'block',
    'position': 'absolute',
    'padding': '15px',
    'top': '10px',
    'right': '15px',
}
header_style = {
    'background': colors['background'],
    'height': '100vh',
    'width': '98vw',
    'position': 'relative',
    'padding-left': '25px',
    'padding-right': '25px',
}
title_style = {
    'textAlign': 'center',
    'color': colors['title'],
    'font-family': ['Palatino Linotype', 'Book Antiqua', 'Palatino', 'serif'],
    'font-size': '65px',
    'letter-spacing': '9px',
    'word-spacing': '10px',
    'font-style': 'normal',
    'font-variant': 'small-caps',
    'text-transform': 'capitalize',
    'width': '100%',
    'display': 'block',
    'border': '3px groove ' + colors['headerBorder'],
    'padding-top': '15px',
    'padding-bottom': '15px'
}
tabs_styles = {
    'width': '75%',
    'margin': 'auto',
    'font-family': fonts['other'],
    'font-size': '35px',
    'align-items': 'center',
    'justify-content': 'center',
    'padding-bottom': '15px',
}
tab_style = {
    'backgroundColor': colors['tabs'],
    'color': colors['tabText'],
    'border': '3px outset ' + colors['tabBorder'],
}
tab_selected_style = {
    # 'borderBottom': '3px ' + colors['tabOutline'],
    'fontWeight': 'bold',
    # 'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': colors['tabSelected'],
    'color': colors['tabSelectedText'],
    'border': '3px inset ' + colors['tabSelectedBorder'],
    'border-top': '0px',
    'border-left': '0px'
}
dropdown_style = {
    'textAlign': 'left',
    'background': colors['dropdown'],
    # 'background-image': 'linear-gradient(#484e55, #3A3F44 60%, #313539)',
    'color': colors['dropdownText'],
    'font-family': fonts['other'],
    'font-size': '20px',
    'border': '1px solid ' + colors['dropdownBorder'],
    'width': '180px',
    # 'padding-top': 5,
    # 'padding-bottom': 5
}
multi_dropdown_style = {
    'textAlign': 'left',
    'background': colors['dropdown'],
    'color': colors['dropdownText'],
    'font-family': fonts['other'],
    'font-size': '20px',
    'border': '1px solid ' + colors['dropdownBorder'],
    'width': '500px',
    # 'padding-top': 5,
    # 'padding-bottom': 5
}
label_style = {
    'font-family': fonts['other'],
    'font-size': '15px',
    'display': 'inline-block',
    'padding-right': 25,
    'padding-top': 10,
    'color': colors['text'],
}
content_style = {
    'width': '100%',
    'border': '3px groove ' + colors['headerBorder'],
    'padding': '10px'
}
price_range_style = {
    'textAlign': 'left',
    'background': colors['dropdown'],
    # 'background-image': 'linear-gradient(#484e55, #3A3F44 60%, #313539)',
    # 'color': colors['dropdownText'],
    'font-family': fonts['other'],
    'font-size': '20px',
    'border': '1px solid ' + colors['dropdownBorder'],
    'width': '180px',
    'padding-top': 5,
    'padding-bottom': 5
}
bed_bath_filter_style = {
    'textAlign': 'center',
    'background': colors['dropdown'],
    # 'background-image': 'linear-gradient(#484e55, #3A3F44 60%, #313539)',
    # 'color': colors['dropdownText'],
    'font-family': fonts['other'],
    'font-size': '20px',
    'border': '1px solid ' + colors['dropdownBorder'],
    'width': '40px',
    'padding-top': 5,
    'padding-bottom': 5,
    'padding-left': 15
}

# Gather data and fix columns
data = gd.gatherData(file_path, file_name)
# data['Website'] = data['URL'].apply(lambda x: gd.getSiteFromURL(x))
# data = data.rename(columns={
#     "Lot Size (m^2)": "LotSize",
#     "Area (m^2)": "Area",
#     "Year Built": "YearBuilt"
# })

# Create DataFrame and drop Null entries
# df = pd.DataFrame(data, columns=['Price', 'LotSize', 'Area', 'Beds', 'Baths', 'YearBuilt',
#                                  'Type', 'Description', 'Dept', 'Agent', 'URL', 'Website', ])
# df = df.dropna()
df = pd.DataFrame(data)

# Columns for different dropdowns
scatterAxes = ['Price', 'Lot Size', 'Area', 'Beds', 'Baths', 'Year Built']
markerSizers = ['Price', 'Lot Size', 'Area', 'Beds', 'Baths']
barXAxes = ['Agent', 'Website', 'Dept', 'Type']
barYAxes = ['Number of Properties', 'Price', 'LotSize', 'Area', 'Beds', 'Baths', 'YearBuilt',
            'Type', 'Website', 'PricePerSqMeterInterior', 'PricePerSqMeterExterior']
listingTypes = ['Casa', 'Land', 'Building', 'Industrial', 'Departamento', 'Office', 'Inmueble',
                'Galpon', 'Barrio', 'Lujosa', 'Storage', 'Penthouse', 'Rural', 'Shed', 'Condo/Apartment',
                'Farm', 'Project', 'Hotel']
typeChoices = ['Casa', 'Land', 'Building', 'Industrial', 'Office']
colorCodingChoices = ['Type', 'Dept', 'Agent', 'Website']

scatter_tab = html.Div([
            html.Div([
                html.Label(
                    [
                        "Select x-axis",
                        dcc.Dropdown(
                            id='scatter-xaxis-attribute',
                            options=[{'label': i, 'value': i} for i in scatterAxes],
                            value='Lot Size',
                            style=dropdown_style,
                        ),
                        dcc.RadioItems(
                            id='scatter-xaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                            value='Linear',
                        )
                    ],
                ),
            ], style=label_style),
            html.Div([
                html.Label(
                    [
                        "Select y-axis",
                        dcc.Dropdown(
                            id='scatter-yaxis-attribute',
                            options=[{'label': i, 'value': i} for i in scatterAxes],
                            value='Price',
                            style=dropdown_style,
                        ),
                        dcc.RadioItems(
                            id='scatter-yaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                            value='Linear',
                            labelStyle={'color': colors['text'], 'display': 'inline-block'}
                        )
                    ],
                ),
            ], style=label_style),
            # html.Div([
            #     html.Label(
            #         [
            #             "Filter by Listing Type",
            #             dcc.Dropdown(
            #                 id='scatter-listing-filter-type',
            #                 options=[{'label': i, 'value': i} for i in listingTypes],
            #                 value='Any',
            #                 style=dropdown_style,
            #             ),
            #             dcc.RadioItems(
            #                 id='scatter-listing-filter-on',
            #                 options=[{'label': i, 'value': i} for i in ['On', 'Off']],
            #                 value='Off',
            #                 labelStyle={'color': colors['text'], 'display': 'inline-block'}
            #             )
            #         ],
            #     ),
            # ], style=label_style),
            html.Div([
                html.Label(
                    [
                        "Datapoint Marker Size",
                        dcc.Dropdown(
                            id='scatter-marker-sizer',
                            options=[{'label': i, 'value': i} for i in markerSizers],
                            value='Lot Size',
                            style=dropdown_style,
                        ),
                        dcc.RadioItems(
                            id='scatter-marker-size-on',
                            options=[{'label': i, 'value': i} for i in ['On', 'Off']],
                            value='Off',
                            labelStyle={'color': colors['text'], 'display': 'inline-block'}
                        )
                    ],
                ),
            ], style=label_style),
            html.Div([
                html.Label(
                    [
                        "Color Coding",
                        dcc.Dropdown(
                            id='scatter-color-coder',
                            options=[{'label': i, 'value': i} for i in colorCodingChoices],
                            value='Type',
                            style=dropdown_style,
                        ),
                        dcc.RadioItems(
                            id='scatter-color-code-on',
                            options=[{'label': i, 'value': i} for i in ['On', 'Off']],
                            value='Off',
                            labelStyle={'color': colors['text'], 'display': 'inline-block'}
                        )
                    ],
                ),
            ], style=label_style),
            html.Br(),
            html.Div([
                html.Label(
                    [
                        "Min Price ($USD)",
                        html.Br(),
                        dcc.Input(
                            id="scatter-min-price", type="number",
                            debounce=True, placeholder="0",
                            min=0, max=100000000, step=25000,
                            style=price_range_style,
                        ),
                    ],
                ),
            ], style=label_style),
            html.Div([
                html.Label(
                    [
                        "Max Price ($USD)",
                        html.Br(),
                        dcc.Input(
                            id="scatter-max-price", type="number",
                            debounce=True, placeholder="1000000",
                            min=0, max=100000000, step=25000,
                            style=price_range_style
                        ),
                    ]
                )

            ], style=label_style),
            html.Div([
                html.Label(
                    [
                        "# Beds",
                        html.Br(),
                        dcc.Input(
                            id="scatter-beds", type="number",
                            debounce=True, placeholder="0",
                            min=0, max=200, step=1,
                            value=0,
                            style=bed_bath_filter_style
                        ),
                    ]
                )

            ], style=label_style),
            html.Div([
                html.Label(
                    [
                        "# Baths",
                        html.Br(),
                        dcc.Input(
                            id="scatter-baths", type="number",
                            debounce=True, placeholder="0",
                            min=0, max=200, step=1,
                            value=0,
                            style=bed_bath_filter_style
                        ),
                    ]
                )

            ], style=label_style),
            html.Br(),
            html.Div([
                html.Label(
                    [
                        "Filter by Listing Type",
                        dcc.Dropdown(
                            id='scatter-listing-filter-type',
                            options=[{'label': i, 'value': i} for i in listingTypes],
                            placeholder="Select Property Types",
                            value=[],
                            multi=True,
                            style=multi_dropdown_style,
                        ),
                    ],
                ),
            ], style=label_style),

            html.Div([
                dcc.Graph(
                    id='scatter-plot',
                    responsive=True,
                    # style={'height': '100%', 'width': '100%', 'float': 'right', 'display': 'inline-block'},
                    style={'height': 900},
                    # animate=True,
                    config=dict(
                        autosizable=True,
                        editable=True,
                        fillFrame=False
                    )
                ),
            ]),
            html.Br(),
        ], style=content_style),

bar_tab = html.Div([
    html.Div([
        html.Label(
            [
                "Select x-axis",
                dcc.Dropdown(
                    id='bar-xaxis-attribute',
                    options=[{'label': i, 'value': i} for i in barXAxes],
                    value='Dept',
                    style=dropdown_style,
                ),
            ],
        ),
    ], style=label_style),
    html.Div([
        html.Label(
            [
                "Select y-axis",
                dcc.Dropdown(
                    id='bar-yaxis-attribute',
                    options=[{'label': i, 'value': i} for i in barYAxes],
                    value='PricePerSqMeterInterior',
                    style=dropdown_style,
                ),
            ],
        ),
    ], style=label_style),
    html.Div([
        dcc.Graph(
            id='bar-chart',
            responsive=True,
            # style={'height': '100%', 'width': '100%', 'float': 'right', 'display': 'inline-block'},
            style={'height': 900},
            # animate=True,
            config=dict(
                autosizable=True,
                editable=True,
                fillFrame=False
            )
        ),
    ]),
], style=content_style)
heatmap_tab = html.Div([
    "Heatmap Go Here"
])
header_layout = html.Div([
    html.Div(
        className="header",
        children=[
            # html.Label(
            #     [
            #         dcc.Dropdown(
            #             id='light-dark-theme',
            #             options=[
            #                 {'label': 'Dark Theme', 'value': 'plotly_dark'},
            #                 {'label': 'Light Theme', 'value': 'plotly_white'},
            #                 # {'label': 'Seaborn', 'value': 'seaborn'}
            #             ],
            #             value='plotly_dark',
            #             # style={
            #             #     # 'background': colors['dropdown'],
            #             #     'color': colors['dropdown_text']
            #             # }
            #         ),
            #     ], style=theme_dropdown_style,
            # ),
            # html.Br(),
            html.Label(
                'Prospector Data Suite',
                style=title_style,
            ),
            html.Br()
        ],
    ),
    dcc.Tabs(id='tabs', value='scatter-tab', className='plot-tab-container', children=[
        dcc.Tab(label='Scatter Plot', value='scatter-tab', children=scatter_tab,
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Bar Chart', value='bar-tab', children=bar_tab,
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Heatmap', value='heatmap-tab', children=heatmap_tab,
                style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content'),
    html.Div(id='clickHidden', hidden=True),
], style=header_style)


app.layout = header_layout


# Scatter Callbacks
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-xaxis-attribute', 'value'),
     Input('scatter-yaxis-attribute', 'value'),
     Input('scatter-xaxis-type', 'value'),
     Input('scatter-yaxis-type', 'value'),
     Input('scatter-listing-filter-type', 'value'),
     # Input('scatter-listing-filter-on', 'value'),
     Input('scatter-marker-sizer', 'value'),
     Input('scatter-marker-size-on', 'value'),
     Input('scatter-color-coder', 'value'),
     Input('scatter-color-code-on', 'value'),
     Input('scatter-min-price', 'value'),
     Input('scatter-max-price', 'value'),
     Input('scatter-beds', 'value'),
     Input('scatter-baths', 'value')
     # Input('light-dark-theme', 'value')
    ])
def update_scatter(xaxis_attr, yaxis_attr,
                   xaxis_type, yaxis_type,
                   type_filter,
                   marker_sizer, marker_size_on,
                   color_coder, color_code_on,
                   min_price, max_price,
                   num_beds, num_baths,
                   template='plotly_dark'):
    title = yaxis_attr + " vs " + xaxis_attr
    fig = gen.Scatter(data=df, title=title, template=template,
                      x=xaxis_attr.replace(' ', ''), y=yaxis_attr.replace(' ', ''),
                      filterType=type_filter,
                      sizeMarkers=marker_size_on, markerSizer=marker_sizer.replace(' ', ''),
                      colorSeries=color_code_on, colorCoder=color_coder.replace(' ', ''),
                      minPrice=min_price, maxPrice=max_price,
                      numBeds=num_beds, numBaths=num_baths)

    fig.update_xaxes(title=xaxis_attr,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_attr,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    gen.format_xaxis(fig, xaxis_attr)
    gen.format_yaxis(fig, yaxis_attr)

    return fig

@app.callback(
    Output('clickHidden', 'hidden'),
    [Input('scatter-plot', 'clickData')])
def display_click_data(clickData):
    if type(clickData) is type(dict()):
        url = clickData['points'][0]['customdata'][0]
        webbrowser.open_new_tab(url)
        # print(str(clickData))
    return True

# Scatter Callbacks
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('bar-xaxis-attribute', 'value'),
     Input('bar-yaxis-attribute', 'value'),
     # Input('scatter-xaxis-type', 'value'),
     # Input('scatter-yaxis-type', 'value'),
     # Input('scatter-listing-filter-type', 'value'),
     # Input('scatter-listing-filter-on', 'value'),
     # Input('scatter-marker-sizer', 'value'),
     # Input('scatter-marker-size-on', 'value'),
     # Input('scatter-color-coder', 'value'),
     # Input('scatter-color-code-on', 'value'),
     # Input('scatter-min-price', 'value'),
     # Input('scatter-max-price', 'value'),
     # Input('scatter-beds', 'value'),
     # Input('scatter-baths', 'value')
     # Input('light-dark-theme', 'value')
    ])
def update_bar(xaxis_attr, yaxis_attr,
                   # xaxis_type, yaxis_type,
                   # type_filter,
                   # marker_sizer, marker_size_on,
                   # color_coder, color_code_on,
                   # min_price, max_price,
                   # num_beds, num_baths,
                   template='plotly_dark'):
    title = yaxis_attr + " vs " + xaxis_attr
    fig = gen.Bar(data=df, title=title, template=template,
                      x=xaxis_attr.replace(' ', ''), y=yaxis_attr.replace(' ', ''),
                      # filterType=type_filter,
                      # sizeMarkers=marker_size_on, markerSizer=marker_sizer.replace(' ', ''),
                      # colorSeries=color_code_on, colorCoder=color_coder.replace(' ', ''),
                      # minPrice=min_price, maxPrice=max_price,
                      # numBeds=num_beds, numBaths=num_baths)
                      )


    gen.format_xaxis(fig, xaxis_attr)
    gen.format_yaxis(fig, yaxis_attr)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
