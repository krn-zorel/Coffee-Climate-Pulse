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
                tooltip={'placement': 'bottom', 'always_visible': False}
            ),
        dcc.Graph(id='choropleth-map', style={'height': '450px'}),
        ]), width=12),
    ]),

    dbc.Row([
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
        ]), md=7)
    ])
   
])