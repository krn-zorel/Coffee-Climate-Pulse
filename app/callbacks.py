from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from app.data import *
from app.tabs.planet import tab_planet




def register_callbacks(app):
    
    # Render selected tab
    @app.callback(Output('tab-content', 'children'), Input('main-tabs', 'value'))
    def render_tab(tab):
        if tab == 'tab-planet':
            return tab_planet
        if tab == 'tab-bean':
            return html.Div("Bean Tab")
        if tab == 'tab-human':
            return html.Div("Human Tab")
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