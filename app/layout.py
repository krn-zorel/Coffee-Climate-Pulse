from dash import html, dcc
import dash_bootstrap_components as dbc
from app.data import YEARS, ENV_COUNTRIES, CHEM_COUNTRIES, C


def card(children):
    return html.Div(children, className="card")

def section_title(text):
    return html.H4(text, className="section-title")

def stat_box(label, value):
    return html.Div([
        html.Div(value, className="stat-value"),
        html.Div(label, className="stat-label")
    ], className="stat-box")



def create_layout():
    # Main div body of html page
    return html.Div([
        # This is the first row containing header and stuff
        # think of it like the header tag fixed at top
        html.Div([
            # only one row inside the header covering whole header
            dbc.Row([
                # column 1 in header
                dbc.Col([
                    html.H1('Coffee Climate Pulse', className="title"),
                    html.P("Planet -> Bean -> Human :: Tracing one chain reaction", className="subtitle")
                ]),
                # column 2 in header
                dbc.Col([
                    dbc.Row([
                        dbc.Col(stat_box('Locations', '25')),
                        dbc.Col(stat_box('Climate rows', '233K')),
                        dbc.Col(stat_box('Quality beans', '1,340')),
                        dbc.Col(stat_box('Health records', '10K')),
                    ], justify='end'),
                ]),
            ], align='center'),
        ], className="header"),

        # this will create interactice tabs buttons
        dcc.Tabs(
            id='main-tabs', value='tab-planet',
            children=[
                dcc.Tab(label='Planet Pulse', value='tab-planet'),
                dcc.Tab(label='Bean Pulse', value='tab-bean'),
                dcc.Tab(label='Human Pulse', value='tab-human'),
            ]
        ),
        html.Div(id='tab-content')
    ],className="main")