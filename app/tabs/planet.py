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
    dbc.Col(card([
        section_title('Yield at Risk - Global Choropleth'),
        html.P('Use')
    ]))
])