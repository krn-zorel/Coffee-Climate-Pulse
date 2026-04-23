from dash import dcc, html
import pandas as pd

# Load processed data for UI dropdowns/sliders
df_planet = pd.read_csv('data/processed/climate_yield.csv')
df_bean = pd.read_csv('data/processed/bean_profile.csv')

def create_layout():
    return html.Div(style={'fontFamily': 'system-ui, sans-serif', 'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'}, children=[
        
        html.Header([
            html.H1("☕ Coffee Climate Pulse", style={'textAlign': 'center', 'color': '#3E2723'}),
            html.P("Tracking the chain reaction from global climate shifts to human physiological response.", 
                   style={'textAlign': 'center', 'color': '#5D4037', 'marginBottom': '30px'})
        ]),
        
        dcc.Tabs(colors={'border': '#d6d6d6', 'primary': '#795548', 'background': '#f9f9f9'}, children=[
            
            # TAB 1: PLANET PULSE
            dcc.Tab(label='🌍 Planet Pulse', children=[
                html.Div([
                    html.H3("Global Production vs. Climate Stress"),
                    dcc.Graph(id='yield-map'),
                    html.Label("Select Year:"),
                    dcc.Slider(
                        id='year-slider',
                        min=df_planet['Year'].min(), max=df_planet['Year'].max(),
                        value=df_planet['Year'].max(), step=1,
                        marks={str(y): str(y) for y in df_planet['Year'].unique() if y % 2 == 0}
                    )
                ], style={'padding': '30px', 'backgroundColor': '#fff', 'borderRadius': '8px', 'marginTop': '10px'})
            ]),

            # TAB 2: BEAN PULSE
            dcc.Tab(label='☕ Bean Pulse', children=[
                html.Div([
                    html.H3("Chemical & Sensory Shift by Origin"),
                    html.Label("Select Origin Country:"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        # Using the exact column name we debugged earlier
                        options=[{'label': c, 'value': c} for c in df_bean['Country of Origin'].unique()],
                        value=df_bean['Country of Origin'].iloc[0]
                    ),
                    dcc.Graph(id='radar-chart')
                ], style={'padding': '30px', 'backgroundColor': '#fff', 'borderRadius': '8px', 'marginTop': '10px'})
            ]),

            # TAB 3: HUMAN PULSE
            dcc.Tab(label='❤️ Human Pulse', children=[
                html.Div([
                    html.H3("Simulated Heart Rate Response"),
                    html.Label("Estimated Caffeine Intake (mg):"),
                    dcc.Slider(
                        id='caffeine-input', 
                        min=0, max=400, step=25, value=95, 
                        marks={0:'0mg', 95:'1 Cup (95mg)', 200:'2 Cups', 400:'High (400mg)'}
                    ),
                    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'height': '300px', 'marginTop': '20px'}, children=[
                        html.Div(id='heart-icon', children="❤️", className='heart-beat'),
                        html.Div(id='heart-rate-output', style={'fontSize': '48px', 'marginLeft': '30px', 'fontWeight': 'bold', 'color': '#D32F2F'})
                    ])
                ], style={'padding': '30px', 'backgroundColor': '#fff', 'borderRadius': '8px', 'marginTop': '10px'})
            ])
        ])
    ])