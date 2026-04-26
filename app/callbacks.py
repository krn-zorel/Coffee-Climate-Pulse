from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from app.data import *
from app.tabs.planet import tab_planet




def register_callbacks(app):
    
    @app.callback(Output('tab-content', 'children'), Input('main-tabs', 'value'))
    def render_tab(tab):
        if tab == 'tab-planet':
            return tab_planet
        if tab == 'tab-bean':
            return html.Div("Bean Tab")
        if tab == 'tab-human':
            return html.Div("Human Tab")
        return html.Div("No tab selected")
    
    @app.callback(Output('choropleth-map', 'figure'), Input('year-slider', 'value'))
    def update_choropleth(year):
        dff = df_fao[df_fao['Year']==year]
        fig=px.choropleth(
            dff, locations='Country', locationmode='country names',
            color='Yield'
        )
        return fig

# from dash import Input, Output, html
# import plotly.express as px
# import plotly.graph_objects as go
# import numpy as np
# import pandas as pd

# from data import *

# def register_callbacks(app):

#     @app.callback(Output('tab-content', 'children'), Input('main-tabs', 'value'))
#     def render_tab(tab):
#         if tab == 'tab-planet':
#             return html.Div("Planet Tab")
#         if tab == 'tab-bean':
#             return html.Div("Bean Tab")
#         if tab == 'tab-human':
#             return html.Div("Human Tab")
#         return html.Div("No tab selected")

#     @app.callback(Output('choropleth-map', 'figure'), Input('year-slider', 'value'))
#     def update_choropleth(year):
#         dff = df_fao[df_fao['Year'] == year]
#         fig = px.choropleth(
#             dff, locations='Country', locationmode='country names',
#             color='Yield'
#         )
#         return fig

#     @app.callback(Output('temp-trend-chart', 'figure'), Input('country-dropdown-env', 'value'))
#     def update_temp_trend(countries):
#         if not countries:
#             return go.Figure()
#         dff = df_env_country[df_env_country['Country'].isin(countries)]
#         fig = px.line(dff, x='YEAR', y='Temp_Avg', color='Country')
#         return fig

#     @app.callback(
#         Output('price-prediction-output', 'children'),
#         [Input('pred-country-env', 'value'),
#          Input('pred-temp', 'value'),
#          Input('pred-prec', 'value'),
#          Input('pred-hum',  'value')]
#     )
#     def predict_price(country, temp, prec, hum):
#         if not country:
#             return ''
#         try:
#             country_data = df_env_country[df_env_country['Country'] == country]
#             price_lag1 = country_data['Price_USD_avg'].iloc[-1] if len(country_data) else 150.0
#             price_lag2 = country_data['Price_USD_avg'].iloc[-2] if len(country_data) > 1 else 140.0
#             temp_lag1  = country_data['Temp_Avg'].iloc[-1] if len(country_data) else temp

#             try:
#                 country_enc = le_env.transform([country])[0]
#             except ValueError:
#                 country_enc = 0

#             row = {
#                 'Country_enc': country_enc,
#                 'Year_norm': 1.0,
#                 'Temp_Avg': temp,
#                 'Temp_Max_avg': temp + 3,
#                 'Temp_Range_avg': 8,
#                 'Humidity_avg': hum,
#                 'Precipitation_total': prec,
#                 'Solar_Radiation_avg': 18,
#                 'Price_lag1': price_lag1,
#                 'Price_lag2': price_lag2,
#                 'Temp_lag1': temp_lag1,
#             }
#             X_pred = pd.DataFrame([{f: row.get(f, 0) for f in price_features}])
#             pred   = float(price_model.predict(X_pred)[0])
#             return html.Div(f"${pred:.0f}")
#         except Exception as e:
#             return html.Div(f'Error: {str(e)}')

#     @app.callback(
#         [Output('hr-display-box', 'children'),
#          Output('current-bpm', 'data')],
#         [Input('cups-slider', 'value'),
#          Input('caffeine-per-cup-slider', 'value'),
#          Input('stress-slider', 'value'),
#          Input('sleep-slider', 'value'),
#          Input('sleep-hours-slider', 'value')]
#     )
#     def predict_heart_rate(cups, caff_per_cup, stress, sleep_q, sleep_hrs):
#         total_caff = cups * caff_per_cup
#         defaults = {
#             'Age': 34, 'Coffee_Intake': cups, 'Caffeine_mg': total_caff,
#             'Sleep_Hours': sleep_hrs, 'BMI': 24,
#             'Physical_Activity_Hours': 7.5,
#             'Sleep_Quality_num': sleep_q,
#             'Stress_Level_num': stress,
#             'Gender_enc': 0, 'Smoking': 0, 'Alcohol_Consumption': 0,
#         }
#         try:
#             row    = {f: defaults.get(f, 0) for f in health_feats}
#             X      = pd.DataFrame([row])[health_feats]
#             X_sc   = health_scaler.transform(X)
#             bpm    = float(hr_model.predict(X_sc)[0])
#         except Exception:
#             bpm = 70

#         return html.Div(f"{bpm:.0f} BPM"), bpm