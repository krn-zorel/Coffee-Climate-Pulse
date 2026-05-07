from dash import html, dcc
import dash_bootstrap_components as dbc
from app.data import YEARS, ENV_COUNTRIES, C, CHEM_COUNTRIES

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
            tooltip=False),
            html.Label('Total Precipitation (mm/yr):', style=LABEL_STYLE),
            dcc.Slider(id='pred-prec', min=500, max=5000, step=100, value=1500,
                       marks={i: str(i) for i in range(500, 5001, 1000)},
                       tooltip=False),
            html.Label('Humidity (%):', style=LABEL_STYLE),
            dcc.Slider(id='pred-hum', min=40, max=98, step=1, value=76,
                       marks={i: str(i) for i in range(40, 99, 20)},
                       tooltip=False),
            html.Div(id='price-prediction-output',
                     style={'marginTop': '16px', 'textAlign': 'center', 'color':'white'}),
        ]), md=5),
    ]),

    
    dbc.Row([
        dbc.Col(card([
            section_title('Price vs Temperature — Scatter'),
            dcc.Graph(id='price-temp-scatter', style={'height': '320px'}),
        ]), md=6),
        dbc.Col(card([
            section_title('Climate Correlation Matrix'),
            dcc.Graph(id='climate-corr-matrix', style={'height': '320px'}),
        ]), md=6),
    ]),
   
], style={'padding': '20px'})


# TAB 2 — BEAN PULSE
# ────────────────────────────────────────────────────────────
tab_bean = html.Div([
    dbc.Row([
        dbc.Col(card([
            section_title('Quality Radar — Harvest Period Comparison'),
            html.P('Earlier vs Later years reveals how the chemical fingerprint of the bean shifts.',
                   style={'color': C['muted'], 'fontSize': '13px', 'marginBottom': '10px'}),
            dcc.RadioItems(
                id='period-radio',
                options=[
                    {'label': '  Earlier years', 'value': 'early'},
                    {'label': '  Later years',   'value': 'late'},
                    {'label': '  Both periods',  'value': 'both'},
                ],
                value='both', inline=True,
                style={'color': C['text'], 'fontSize': '13px', 'marginBottom': '10px'}
            ),
            dcc.Graph(id='radar-period-chart', style={'height': '400px'}),
        ]), md=6),

        dbc.Col(card([
            section_title('Arabica vs Robusta Profiles'),
            dcc.Graph(id='radar-species-chart', style={'height': '400px'}),
        ]), md=6),
    ]),

    dbc.Row([
        dbc.Col(card([
            section_title('Cup Quality by Country — Box Plot'),
            dcc.Dropdown(
                id='quality-country-dropdown',
                options=[{'label': c, 'value': c} for c in CHEM_COUNTRIES],
                value=sorted(CHEM_COUNTRIES)[:6],
                multi=True, style=DROPDOWN_STYLE,
            ),
            dcc.Graph(id='quality-box-plot', style={'height': '340px'}),
        ]), md=7),

        dbc.Col(card([
            section_title('Top Countries — Avg Score'),
            dcc.Graph(id='top-countries-bar', style={'height': '340px'}),
        ]), md=5),
    ]),

    dbc.Row([
        dbc.Col(card([
            section_title('Altitude vs Cup Score'),
            dcc.Graph(id='altitude-scatter', style={'height': '320px'}),
        ]), md=6),
        dbc.Col(card([
            section_title('Quality Attribute Correlation'),
            dcc.Graph(id='quality-corr-heatmap', style={'height': '320px'}),
        ]), md=6),
    ]),
], style={'padding': '20px'})

# ────────────────────────────────────────────────────────────
# TAB 3 — HUMAN PULSE
# ────────────────────────────────────────────────────────────
tab_human = html.Div([
    dbc.Row([
        dbc.Col(card([
            section_title('Live Heartbeat Simulator'),
            html.P(
                'Adjust the coffee profile. The heartbeat responds in real time.',
                style={'color': C['muted'], 'fontSize': '13px', 'marginBottom': '12px'}
            ),
            dbc.Row([
                dbc.Col([
                    html.Label('Cups of coffee / day:', style=LABEL_STYLE),
                    dcc.Slider(id='cups-slider', min=0, max=10, step=0.5, value=2,
                               marks={i: str(i) for i in range(0, 11, 2)},
                               tooltip=False),
                    html.Label('Caffeine per cup (mg):', style=LABEL_STYLE),
                    dcc.Slider(id='caffeine-per-cup-slider', min=0, max=200, step=10, value=80,
                               marks={i: str(i) for i in range(0, 201, 50)},
                               tooltip=False),
                    html.Label('Stress level:', style=LABEL_STYLE),
                    dcc.Slider(id='stress-slider', min=1, max=3, step=1, value=1,
                               marks={1: 'Low', 2: 'Medium', 3: 'High'},tooltip=False),
                    html.Label('Sleep quality:', style=LABEL_STYLE),
                    dcc.Slider(id='sleep-slider', min=1, max=4, step=1, value=3,
                               marks={1: 'Poor', 2: 'Fair', 3: 'Good', 4: 'Excellent'},tooltip=False),
                    html.Label('Hours of sleep / night:', style=LABEL_STYLE),
                    dcc.Slider(id='sleep-hours-slider', min=3, max=10, step=0.5, value=7,
                               marks={i: str(i) for i in range(3, 11, 2)},
                               tooltip=False),
                ], md=7),
                dbc.Col([
                    html.Div(id='hr-display-box', style={
                        'textAlign': 'center',
                        'padding': '24px 0',
                    }),
                    dcc.Graph(id='heartbeat-graph', style={'height': '200px'}),
                    dcc.Interval(id='heartbeat-interval', interval=60, n_intervals=0),
                    dcc.Store(id='current-bpm', data=70),
                ], md=5),
            ]),
        ]), md=7),

        dbc.Col(card([
            section_title('Caffeine vs Heart Rate — Scatter'),
            dcc.Graph(id='caffeine-hr-scatter', style={'height': '480px'}),
        ]), md=5),
    ]),

    dbc.Row([
        dbc.Col(card([
            section_title('Heatmap — Caffeine × Sleep Quality → Heart Rate'),
            dcc.Graph(id='health-heatmap', style={'height': '340px'}),
        ]), md=6),
        dbc.Col(card([
            section_title('3D: Caffeine · Sleep · Heart Rate'),
            dcc.Graph(id='scatter-3d', style={'height': '340px'}),
        ]), md=6),
    ]),

    dbc.Row([
        dbc.Col(card([
            section_title('Heart Rate by Stress Level & Cups / Day'),
            dcc.Graph(id='stress-cups-violin', style={'height': '320px'}),
        ]), md=6),
        dbc.Col(card([
            section_title('Caffeine Intake Distribution by Country'),
            dcc.Graph(id='caffeine-country-box', style={'height': '320px'}),
        ]), md=6),
    ]),
], style={'padding': '20px'})