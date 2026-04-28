from dash import html, dcc
import dash_bootstrap_components as dbc
from app.data import YEARS, ENV_COUNTRIES, C

from app.layout import card, section_title, stat_box

SLIDER_STYLE = {'color': C['text'], 'fontSize': '12px'}
LABEL_STYLE  = {'color': C['muted'], 'fontSize': '12px',
                'marginTop': '10px', 'marginBottom': '4px'}
DROPDOWN_STYLE = {'backgroundColor': '#1F1F1F', 'color': '#000', 'fontSize': '13px'}


## Tab 1 - Planet Pulse
tab_planet = html.Div([

    #Choropleth Map
    dbc.Row([
        dbc.Col(card([
        section_title('Yield at Risk - Global Choropleth'),
        html.P('Use the slider to travel through time. Warmer colours = lower yield per hectare.'),
        html.Label('Select Year: ', style=LABEL_STYLE),
        dcc.Slider(
                id='year-slider',
                min=int(min(YEARS)),
                max=int(max(YEARS)), 
                step=1,
                value=int(max(YEARS) - 2),
                marks={int(y): {
                    "label": str(int(y)),
                    "style":{"color":"white"}
                }for y in YEARS[::5]},
                tooltip=False,
                updatemode='drag',
        ),
        dcc.Graph(id='choropleth-map', style={'height': '450px','marginTop':'30px'}),
        ]), width=12),
    ]),

    dbc.Row([

    # Temp Trend Chart
        dbc.Col(card([
            section_title('Temperature Trend by Country'),
            dcc.Dropdown(
                id='country-dropdown-env',
                options=[{'label':c, 'value':c} for c in ENV_COUNTRIES],
                value=ENV_COUNTRIES[:4],
                multi=True,
                style=DROPDOWN_STYLE,
            ),
            dcc.Graph(id='temp-trend-chart', style={'height':'320px'}),
        ]), md=7),

        # Coffee Price Predictor by Climate
        dbc.Col(card([
            section_title('Climate → Price Predictor'),
            html.P('Predcit coffee price from climate inputs using the GBR model.',
            style={'color':C['muted'],'fontSize':'12px'}),
            html.Label('Country:',
            style=LABEL_STYLE),
            dcc.Dropdown(
                id='pred-country-env',
                options=[{'label':c,'value:':c}for c in ENV_COUNTRIES],
                value=ENV_COUNTRIES[0],
                style=DROPDOWN_STYLE,
            ),
            html.Label('Avg Temperature (°C):',style=LABEL_STYLE),
            dcc.Slider(id='pred-temp',min=10,max=35,step=0.5,value=24,
            marks={i:str(i) for i in range(10,36,5)},
            # tooltip={'always_visible':False})
            tooltip=False),

        ])),
    ])
   
])