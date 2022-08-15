import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'Farmers Delight'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/ksebastian/306-agriculture-exports-dropdown'
# here's the list of possible columns to choose from.
list_of_columns = ['Baked goods, cereals, and pasta',
                   'Beef and beef products',
                   'Beer',
                   'Chocolate and cocoa products',
                   'Coarse grains (including corn)',
                   'Cocoa beans',
                   'Cocoa paste and cocoa butter',
                   'Coffee, unroasted',
                   'Condiments and sauces',
                   'Dairy products',
                   'Dextrins, peptones, and proteins',
                   'Distilled spirits',
                   'Dog and cat food',
                   'Essential oils',
                   'Ethanol (non-bev.)',
                   'Food preparations',
                   'Fresh fruit - avocados',
                   'Fresh fruit - bananas',
                   'Fresh fruit - berries',
                   'Fresh fruit - other',
                   'Fresh vegetables',
                   'Fruit and vegetable juices',
                   'Industrial alcohols and fatty acids',
                   'Live animals',
                   'Mfg. tobacco',
                   'Non-alcoholic bev. (ex. juices)',
                   'Nursery products and cut flowers',
                   'Oilseed meal and cake',
                   'Oilseeds',
                   'Other feeds and grain products',
                   'Other livestock products',
                   'Other meat products',
                   'Planting seeds',
                   'Pork and pork products',
                   'Poultry products and eggs',
                   'Processed fruit and vegetables',
                   'Pulses',
                   'Raw beet and cane sugar',
                   'Rice',
                   'Roasted and instant coffee',
                   'Spices',
                   'Sugars, sweeteners, bev. bases',
                   'Tea',
                   'Tobacco, unmanufactured',
                   'Tree nuts',
                   'Vegetable oils',
                   'Wheat',
                   'Wine and related products',
                   'Yeast and baking powder']

########## Set up the chart

import pandas as pd

df = pd.read_csv('assets/usa-imports-2021.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('2021 Agricultural Imports, by State'),
    html.Div([
        html.Div([
            html.H6('Select a variable for analysis:'),
            dcc.Dropdown(
                id='options-drop',
                options=[{'label': i, 'value': i} for i in list_of_columns],
                value='Beer'
            ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
                  ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
              [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Imports of {varname} in 2021'
    mycolorscale = 'ylorrd'  # Note: The error message will list possible color scales.
    mycolorbartitle = "USD"

    data = go.Choropleth(
        locations=df['State'],  # Spatial coordinates
        locationmode='USA-states',  # set of locations match entries in `locations`
        z=df[varname].astype(float),  # Data to be color-coded
        colorscale=mycolorscale,
        colorbar_title=mycolorbartitle,
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text=mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
