from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import joblib

# Load Data and Model into memory
df_planet = pd.read_csv('data/processed/climate_yield.csv')
df_bean = pd.read_csv('data/processed/bean_profile.csv')
pulse_model = joblib.load('models/pulse_model.pkl')

def register_callbacks(app):
    
    # 1. Map Callback
    @app.callback(
        Output('yield-map', 'figure'),
        Input('year-slider', 'value')
    )
    def update_map(selected_year):
        filtered_df = df_planet[df_planet['Year'] == selected_year]
        fig = px.choropleth(filtered_df, locations="Country", locationmode="country names", 
                            color="Yield", hover_data=["Temperature"],
                            color_continuous_scale="YlOrBr")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    # 2. Radar Chart Callback
    @app.callback(
        Output('radar-chart', 'figure'),
        Input('country-dropdown', 'value')
    )
    def update_radar(selected_country):
        # Filter for the selected country
        country_data = df_bean[df_bean['Country of Origin'] == selected_country].iloc[0]
        
        metrics = ['Aroma', 'Flavor', 'Acidity', 'Body', 'Balance']
        values = [country_data[m] for m in metrics]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=values, theta=metrics, fill='toself', line_color='#795548'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[6, 9])), showlegend=False)
        return fig

    # 3. Heartbeat Animation Callback
    @app.callback(
        [Output('heart-rate-output', 'children'),
         Output('heart-icon', 'style')],
        Input('caffeine-input', 'value')
    )
    def update_pulse(caffeine):
        # Predict BPM using your trained model!
        # Need to format it exactly as the model expects (a 2D array/DataFrame)
        prediction_df = pd.DataFrame([[caffeine]], columns=['Caffeine_mg'])
        bpm = pulse_model.predict(prediction_df)[0]
        
        # Calculate animation speed (higher BPM = faster CSS animation)
        duration = 60 / bpm
        style = {
            'fontSize': '120px',
            'animation': f'beat {duration}s infinite',
            'transformOrigin': 'center'
        }
        
        return f"{int(bpm)} BPM", style