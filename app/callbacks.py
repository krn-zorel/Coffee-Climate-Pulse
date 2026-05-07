from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from app.data import *
from app.tabs.planet import tab_planet, tab_bean, tab_human




def register_callbacks(app):
    
    # Render selected tab
    @app.callback(Output('tab-content', 'children'), Input('main-tabs', 'value'))
    def render_tab(tab):
        if tab == 'tab-planet':
            return tab_planet
        if tab == 'tab-bean':
            return tab_bean
        if tab == 'tab-human':
            return tab_human
        return html.Div("No tab selected")
    
    # This has all the callbacks for planet tab
    #----------------------------------------------
    @app.callback(Output('choropleth-map', 'figure'), Input('year-slider', 'value'))
    def update_choropleth(year):
        dff = df_fao[df_fao['Year']==year]
        fig=px.choropleth(
            dff, locations='Country', locationmode='country names',
            color='Yield', color_continuous_scale='YlOrRd',
            range_color=[df_fao['Yield'].quantile(0.05),df_fao['Yield'].quantile(0.95)],
            labels={'Yield':'Yield (Hg/Ha)'},
            title=f'Global Coffee Yield - {year}',
            hover_name='Country', hover_data={'Yield':':.0f'},
        )
        fig.update_layout(
            paper_bgcolor = C['bg'], plot_bgcolor=C['bg'], font_color=C['text'],
            geo=dict(bgcolor=C['bg'], showframe=False,
                     showcoastlines=True,
                     coastlinecolor='#333',showland=True,
                     landcolor='#1A1A1A',
                     showocean=True,
                     oceancolor='#111'),
                     margin=dict(l=0, r=0, t=40, b=0),
                     coloraxis_colorbar=dict(tickfont=dict(color=C['text']),
                    title='Hg/Ha'),
        )
        return fig

    @app.callback(Output('temp-trend-chart','figure'),Input('country-dropdown-env','value'))
    def updata_temp_trend(countries):
        if not countries:
            return go.Figure()
        dff = df_env_country[df_env_country['Country'].isin(countries)]
        fig = px.line(
            dff,  x='YEAR', y='Temp_Avg',color='Country',
            title='Average Temperature Trend by Country',
            labels={'Temp_Avg':'Avg Temp(°C)','YEAR':'Year'},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(paper_bgcolor=C['card'],
        plot_bgcolor=C['card'],
        font_color=C['text'],
        hovermode='x unified',
        legend=dict(font=dict(color=C['text'])),
        margin=dict(l=0, r=0, t=40,b=0)
        )
        fig.update_traces(line_width=2)
        return fig
    
        
    @app.callback(
        Output('price-prediction-output', 'children'),
        [Input('pred-country-env', 'value'),
        Input('pred-temp', 'value'),
        Input('pred-prec', 'value'),
        Input('pred-hum',  'value')]
    )
    def predict_price(country, temp, prec, hum):
        if not country:
            return ''
        try:
            country_data = df_env_country[df_env_country['Country'] == country]
            price_lag1 = country_data['Price_USD_avg'].iloc[-1] if len(country_data) else 150.0
            price_lag2 = country_data['Price_USD_avg'].iloc[-2] if len(country_data) > 1 else 140.0
            temp_lag1  = country_data['Temp_Avg'].iloc[-1] if len(country_data) else temp

            try:
                country_enc = le_env.transform([country])[0]
            except ValueError:
                country_enc = 0

            row = {
                'Country_enc':           country_enc,
                'Year_norm':             1.0,
                'Temp_Avg':              temp,
                'Temp_Max_avg':          temp + 3,
                'Temp_Range_avg':        8,
                'Humidity_avg':          hum,
                'Precipitation_total':   prec,
                'Solar_Radiation_avg':   18,
                'Price_lag1':            price_lag1,
                'Price_lag2':            price_lag2,
                'Temp_lag1':             temp_lag1,
            }
            X_pred = pd.DataFrame([{f: row.get(f, 0) for f in price_features}])
            pred   = float(price_model.predict(X_pred)[0])
            pred   = max(50, min(600, pred))

            color = C['green'] if pred < 150 else C['accent'] if pred < 250 else C['red']
            return html.Div([
                html.Div(f'${pred:.0f}', style={'fontSize': '36px', 'fontWeight': 'bold',
                                                'color': color}),
                html.Div('Predicted price (USD / 60 kg)', style={'color': C['muted'],
                                                                'fontSize': '12px'}),
                html.Div(f'{country}  ·  {temp:.1f}°C  ·  {prec:.0f}mm',
                        style={'color': C['muted'], 'fontSize': '11px', 'marginTop': '4px'}),
            ])
        except Exception as e:
            return html.Div(f'Error: {str(e)}', style={'color': C['red']})


    @app.callback(Output('price-temp-scatter', 'figure'), Input('main-tabs', 'value'))
    def update_price_temp_scatter(tab):
        if tab != 'tab-planet':
            return go.Figure()
        fig = px.scatter(
            df_env_country, x='Temp_Avg', y='Price_USD_avg',
            color='Country', size='Precipitation_total',
            animation_frame='YEAR',
            hover_data=['Country', 'YEAR'],
            labels={'Temp_Avg': 'Avg Temp (°C)', 'Price_USD_avg': 'Price (USD/60kg)'},
            color_discrete_sequence=px.colors.qualitative.Set2,
            title='Temperature vs Price (animated by year)',
        )
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], margin=dict(l=0,r=0,t=40,b=0))
        return fig


    @app.callback(Output('climate-corr-matrix', 'figure'), Input('main-tabs', 'value'))
    def update_climate_corr(tab):
        if tab != 'tab-planet':
            return go.Figure()
        cols = ['Temp_Avg', 'Temp_Max_avg', 'Humidity_avg',
                'Precipitation_total', 'Solar_Radiation_avg', 'Price_USD_avg']
        cols = [c for c in cols if c in df_env_country.columns]
        corr = df_env_country[cols].corr().round(2)
        fig  = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale='RdBu', zmid=0,
            text=corr.values, texttemplate='%{text:.2f}',
            hovertemplate='%{x} vs %{y}: %{z:.2f}<extra></extra>',
        ))
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], margin=dict(l=0,r=0,t=30,b=0),
                        title='Climate Correlations')
        return fig
    


    # This one are the callbacks for bean tab


        
    def _make_radar(species_or_period_groups, colors, range_min=6.5, title=''):
        fig = go.Figure()
        for label, avg, color in species_or_period_groups:
            if avg is None:
                continue
            cols = [c for c in radar_cols if c in avg.index]
            vals = avg[cols].tolist() + [avg[cols].iloc[0]]
            cats = cols + [cols[0]]
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=cats, fill='toself', name=label,
                line_color=color, opacity=0.72, line_width=2,
            ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[range_min, 10],
                                gridcolor='#333', linecolor='#555',
                                tickfont=dict(color=C['text'])),
                angularaxis=dict(tickfont=dict(color=C['text']), linecolor='#555'),
                bgcolor=C['card'],
            ),
            paper_bgcolor=C['card'], font_color=C['text'],
            showlegend=True, title=title,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        return fig


    @app.callback(Output('radar-period-chart', 'figure'), Input('period-radio', 'value'))
    def update_radar_period(period):
        df_r = df_chem.dropna(subset=['Year'])
        yr_med = df_r['Year'].median()
        df_r['Period'] = np.where(df_r['Year'] >= yr_med, 'Later', 'Earlier')

        groups = []
        if period in ('early', 'both'):
            sub = df_r[df_r['Period'] == 'Earlier']
            if len(sub):
                groups.append(('Earlier years', sub[radar_cols].mean(), C['blue']))
        if period in ('late', 'both'):
            sub = df_r[df_r['Period'] == 'Later']
            if len(sub):
                groups.append(('Later years',   sub[radar_cols].mean(), C['red']))

        return _make_radar(groups, [], title=f'Quality Shift — Earlier vs Later Years (split ≈{int(yr_med)})')


    @app.callback(Output('radar-species-chart', 'figure'), Input('main-tabs', 'value'))
    def update_radar_species(tab):
        if tab != 'tab-bean':
            return go.Figure()
        groups = []
        for sp, color in [('Arabica', '#8B6914'), ('Robusta', C['red'])]:
            if 'Species' in df_chem.columns:
                sub = df_chem[df_chem['Species'] == sp]
            else:
                sub = df_chem if sp == 'Arabica' else pd.DataFrame()
            if len(sub):
                groups.append((sp, sub[radar_cols].mean(), color))
        return _make_radar(groups, [], title='Arabica vs Robusta Flavour Profiles')


    @app.callback(Output('quality-box-plot', 'figure'), Input('quality-country-dropdown', 'value'))
    def update_quality_box(countries):
        if not countries or 'Total Cup Points' not in df_chem.columns:
            return go.Figure()
        dff = df_chem[df_chem['Country'].isin(countries)]
        fig = px.box(dff, x='Country', y='Total Cup Points', color='Country',
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    title='Cup Score Distribution by Country')
        fig.add_hline(y=80, line_dash='dash', line_color='gray', annotation_text='Specialty (80)')
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], showlegend=False,
                        margin=dict(l=0,r=0,t=40,b=0))
        return fig


    @app.callback(Output('top-countries-bar', 'figure'), Input('main-tabs', 'value'))
    def update_top_countries_bar(tab):
        if tab != 'tab-bean' or 'Total Cup Points' not in df_chem.columns:
            return go.Figure()
        top = (df_chem.groupby('Country')['Total Cup Points']
                    .agg(['mean','count'])
                    .query('count >= 5')
                    .sort_values('mean', ascending=True)
                    .tail(12).reset_index())
        fig = px.bar(top, x='mean', y='Country', orientation='h',
                    color='mean', color_continuous_scale='YlOrBr',
                    title='Top 12 Countries — Avg Cup Score',
                    labels={'mean': 'Avg Score', 'Country': ''})
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], showlegend=False,
                        margin=dict(l=0,r=0,t=40,b=0),
                        coloraxis_showscale=False)
        return fig


    @app.callback(Output('altitude-scatter', 'figure'), Input('main-tabs', 'value'))
    def update_altitude_scatter(tab):
        if tab != 'tab-bean' or 'altitude_mean_meters' not in df_chem.columns:
            return go.Figure()
        dff = df_chem.dropna(subset=['altitude_mean_meters', 'Total Cup Points'])
        fig = px.scatter(dff, x='altitude_mean_meters', y='Total Cup Points',
                        color='Species' if 'Species' in dff.columns else None,
                        opacity=0.5, trendline='ols',
                        color_discrete_map={'Arabica': '#8B6914', 'Robusta': C['red']},
                        title='Altitude vs Cup Score',
                        labels={'altitude_mean_meters': 'Altitude (m)',
                                'Total Cup Points': 'Score'})
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], margin=dict(l=0,r=0,t=40,b=0))
        return fig


    @app.callback(Output('quality-corr-heatmap', 'figure'), Input('main-tabs', 'value'))
    def update_quality_corr(tab):
        if tab != 'tab-bean':
            return go.Figure()
        cols = [c for c in radar_cols + ['Total Cup Points'] if c in df_chem.columns]
        corr = df_chem[cols].corr().round(2)
        fig  = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale='YlOrBr',
            text=corr.values, texttemplate='%{text:.2f}',
        ))
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], margin=dict(l=0,r=0,t=30,b=0),
                        title='Quality Attribute Correlations')
        return fig
    


    # this are all the callbacks for human tab
        
    @app.callback(
        [Output('hr-display-box', 'children'),
        Output('current-bpm', 'data')],
        [Input('cups-slider', 'value'),
        Input('caffeine-per-cup-slider', 'value'),
        Input('stress-slider', 'value'),
        Input('sleep-slider', 'value'),
        Input('sleep-hours-slider', 'value')]
    )
    def predict_heart_rate(cups, caff_per_cup, stress, sleep_q, sleep_hrs):
        total_caff = cups * caff_per_cup
        defaults = {
            'Age': 34, 'Coffee_Intake': cups, 'Caffeine_mg': total_caff,
            'Sleep_Hours': sleep_hrs, 'BMI': 24,
            'Physical_Activity_Hours': 7.5,
            'Sleep_Quality_num': sleep_q,
            'Stress_Level_num': stress,
            'Gender_enc': 0, 'Smoking': 0, 'Alcohol_Consumption': 0,
        }
        try:
            row    = {f: defaults.get(f, 0) for f in health_feats}
            X      = pd.DataFrame([row])[health_feats]
            X_sc   = health_scaler.transform(X)
            bpm    = float(hr_model.predict(X_sc)[0])
            bpm    = max(45, min(180, bpm))
        except Exception:
            bpm = 70 + total_caff * 0.015

        color = C['blue'] if bpm < 65 else C['green'] if bpm < 75 \
                else C['accent'] if bpm < 90 else C['red']
        label = ('Resting 🟢' if bpm < 65 else 'Normal 🟢' if bpm < 80
                else 'Elevated 🟡' if bpm < 100 else 'High 🔴')

        display = html.Div([
            html.Div(f'{bpm:.0f}', style={'fontSize': '60px', 'fontWeight': 'bold',
                                        'color': color, 'lineHeight': '1',
                                        'fontFamily': 'Georgia, serif'}),
            html.Div('BPM', style={'fontSize': '16px', 'color': C['muted'], 'letterSpacing': '3px'}),
            html.Div(label, style={'fontSize': '13px', 'color': color, 'marginTop': '6px'}),
            html.Div(f'Caffeine: {total_caff:.0f} mg/day  ·  {cups} cups',
                    style={'fontSize': '11px', 'color': C['muted'], 'marginTop': '6px'}),
        ])
        return display, bpm


    @app.callback(
        Output('heartbeat-graph', 'figure'),
        [Input('heartbeat-interval', 'n_intervals'),
        Input('current-bpm', 'data')]
    )
    def animate_heartbeat(n, bpm):
        bpm = bpm or 70
        beat_period = 60.0 / bpm
        t   = np.linspace(0, 4, 1000)
        ecg = np.zeros_like(t)

        for bt in np.arange(0, 4, beat_period):
            ecg += 0.07 * np.exp(-((t - (bt + 0.06))**2) / 0.0008)   # P
            ecg -= 0.06 * np.exp(-((t - (bt + 0.15))**2) / 0.0002)   # Q
            ecg += 1.00 * np.exp(-((t - (bt + 0.18))**2) / 0.00007)  # R
            ecg -= 0.22 * np.exp(-((t - (bt + 0.22))**2) / 0.0001)   # S
            ecg += 0.22 * np.exp(-((t - (bt + 0.38))**2) / 0.0020)   # T

        ecg += np.random.normal(0, 0.004, len(t))
        # Scroll via offset
        offset = (n * 0.05) % beat_period
        t_disp = t - offset

        color = (C['blue'] if bpm < 65 else C['green'] if bpm < 75
                else C['accent'] if bpm < 90 else C['red'])

        fig = go.Figure(go.Scatter(
            x=t_disp, y=ecg, mode='lines',
            line=dict(color=color, width=1.5),
        ))
        fig.update_layout(
            paper_bgcolor=C['card'], plot_bgcolor=C['card'],
            xaxis=dict(visible=False, range=[0, 4]),
            yaxis=dict(visible=False, range=[-0.5, 1.4]),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
        )
        return fig


    @app.callback(Output('caffeine-hr-scatter', 'figure'), Input('main-tabs', 'value'))
    def update_caffeine_hr_scatter(tab):
        if tab != 'tab-human':
            return go.Figure()
        fig = px.scatter(
            df_health.sample(min(3000, len(df_health)), random_state=42),
            x='Caffeine_mg', y='Heart_Rate',
            color='Stress_Level', symbol='Sleep_Quality',
            color_discrete_map={'Low': C['green'], 'Medium': C['accent'], 'High': C['red']},
            opacity=0.45, trendline='ols',
            title='Caffeine → Heart Rate  (coloured by Stress)',
            labels={'Caffeine_mg': 'Caffeine (mg/day)', 'Heart_Rate': 'Heart Rate (BPM)'},
        )
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], margin=dict(l=0,r=0,t=40,b=0))
        return fig


    @app.callback(Output('health-heatmap', 'figure'), Input('main-tabs', 'value'))
    def update_health_heatmap(tab):
        if tab != 'tab-human':
            return go.Figure()
        df_h = df_health.copy()
        df_h['Caffeine_bin'] = pd.cut(df_h['Caffeine_mg'],
                                    bins=[0,100,200,300,400,800],
                                    labels=['0–100','101–200','201–300','301–400','400+'])
        sq_order = ['Poor','Fair','Good','Excellent']
        pivot = df_h.groupby(['Caffeine_bin','Sleep_Quality'], observed=True)['Heart_Rate'] \
                    .mean().unstack()
        pivot = pivot[[c for c in sq_order if c in pivot.columns]]

        fig = go.Figure(go.Heatmap(
            z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale='YlOrRd',
            text=np.round(pivot.values, 1), texttemplate='%{text}',
            hovertemplate='Caffeine: %{y}<br>Sleep: %{x}<br>Mean HR: %{z:.1f} BPM<extra></extra>',
        ))
        fig.update_layout(
            title='Mean Heart Rate — Caffeine × Sleep Quality',
            xaxis_title='Sleep Quality', yaxis_title='Caffeine (mg/day)',
            paper_bgcolor=C['card'], plot_bgcolor=C['card'], font_color=C['text'],
            margin=dict(l=0,r=0,t=40,b=0),
        )
        return fig


    @app.callback(Output('scatter-3d', 'figure'), Input('main-tabs', 'value'))
    def update_3d_scatter(tab):
        if tab != 'tab-human':
            return go.Figure()
        s = df_health.sample(min(2000, len(df_health)), random_state=42)
        fig = px.scatter_3d(
            s, x='Caffeine_mg', y='Sleep_Hours', z='Heart_Rate',
            color='Heart_Rate', color_continuous_scale='YlOrRd', opacity=0.45,
            labels={'Caffeine_mg':'Caffeine (mg)','Sleep_Hours':'Sleep (hrs)','Heart_Rate':'HR (BPM)'},
            title='Caffeine · Sleep · Heart Rate',
        )
        fig.update_traces(marker=dict(size=2.5))
        fig.update_layout(
            paper_bgcolor=C['card'], font_color=C['text'],
            scene=dict(
                xaxis=dict(backgroundcolor=C['card'], gridcolor='#2A2A2A', zerolinecolor='#333'),
                yaxis=dict(backgroundcolor=C['card'], gridcolor='#2A2A2A', zerolinecolor='#333'),
                zaxis=dict(backgroundcolor=C['card'], gridcolor='#2A2A2A', zerolinecolor='#333'),
            ),
            margin=dict(l=0,r=0,t=40,b=0),
        )
        return fig


    @app.callback(Output('stress-cups-violin', 'figure'), Input('main-tabs', 'value'))
    def update_stress_violin(tab):
        if tab != 'tab-human':
            return go.Figure()
        df_h = df_health.copy()
        df_h['Cups_round'] = df_h['Coffee_Intake'].round().clip(0, 7).astype(int)
        fig = px.violin(
            df_h, x='Stress_Level', y='Heart_Rate',
            color='Stress_Level', box=True, points=False,
            category_orders={'Stress_Level': ['Low','Medium','High']},
            color_discrete_map={'Low': C['green'], 'Medium': C['accent'], 'High': C['red']},
            title='Heart Rate Distribution by Stress Level',
            labels={'Heart_Rate': 'Heart Rate (BPM)', 'Stress_Level': 'Stress Level'},
        )
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], showlegend=False,
                        margin=dict(l=0,r=0,t=40,b=0))
        return fig


    @app.callback(Output('caffeine-country-box', 'figure'), Input('main-tabs', 'value'))
    def update_caffeine_country(tab):
        if tab != 'tab-human':
            return go.Figure()
        top_countries = (df_health.groupby('Country')['Caffeine_mg']
                                .median().nlargest(10).index.tolist())
        dff = df_health[df_health['Country'].isin(top_countries)]
        fig = px.box(
            dff, x='Country', y='Caffeine_mg', color='Country',
            color_discrete_sequence=px.colors.qualitative.Set2,
            title='Caffeine Intake by Country (Top 10 by median)',
            labels={'Caffeine_mg': 'Caffeine (mg/day)', 'Country': ''},
        )
        fig.update_layout(paper_bgcolor=C['card'], plot_bgcolor=C['card'],
                        font_color=C['text'], showlegend=False,
                        margin=dict(l=0,r=0,t=40,b=0))
        fig.update_xaxes(tickangle=30)
        return fig