# !/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from datetime import datetime
import numpy as np
from sqlalchemy import create_engine

import pandas as pd

db_config = {'user': 'my_user',         
                 'pwd': 'my_user_password', 
                 'host': 'localhost',       
                 'port': 5432,              
                 'db': 'zen'}             
    
connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
                                     db_config['pwd'],
                                 db_config['host'],
                                 db_config['port'],
                                 db_config['db'])
engine = create_engine(connection_string)

query = ''' SELECT *
        FROM dash_visits
        '''
        
dash_visits = pd.io.sql.read_sql(query, con = engine)

query = ''' SELECT *
        FROM dash_engagement
        '''
        
dash_engagement = pd.io.sql.read_sql(query, con = engine)

dash_visits['dt'] = pd.to_datetime(dash_visits['dt'])
dash_engagement['dt'] = pd.to_datetime(dash_engagement['dt'])

dash_visits['dt'] = pd.to_datetime(dash_visits['dt'], format = '%Y-%m-%d %h:%m:%s')
dash_engagement['dt'] = pd.to_datetime(dash_engagement['dt'], format = '%Y-%m-%d %h:%m:%s')

# задаём лейаут
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[

    #формируем html
    html.H1(children = 'Yandex Zen: users interactions with cards'),
    html.Div('''
        This dashboard shows the history and details of user interaction with Yandex Zen cards. Use filters for card themes, age groups, and time of visit to select the desired options.
    '''),
    html.Br(),
    
    html.Div([
    
        html.Div([
    
            html.Label('Date & time:'),
            dcc.DatePickerRange(
                start_date = dash_visits['dt'].min(),
                end_date = dash_visits['dt'].max(),
                display_format = 'YYYY-MM-DD HH:SS',
                id = 'dt_selector',       
            ),
            
            html.Label('Select age categories:'),
            dcc.Dropdown( 
                id = 'age-dropdown',
                options = [{'label': x,  
                            'value': x} for x in dash_visits['age_segment'].unique()], 
                value = dash_visits['age_segment'].unique(),
                multi = True)

        ], className = 'four columns'),
        
        html.Div([
            html.Label('Select a set of card themes:'),
            dcc.Dropdown( 
                id = 'item-topic-dropdown',
                options = [{'label': x,  
                            'value': x} for x in dash_visits['item_topic'].unique()], 
                value = dash_visits['item_topic'].unique(),
                multi = True)
        ], className = 'eight columns')
        ], className = 'row'),
        
        html.Br(),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div([
                html.Label('History of events on the themes of the cards(all topics events):'),
                dcc.Graph(
                id = 'history-absolute-visits',
                style = {'height': '50vw'}
                )
            ], className = 'six columns'),
            
            html.Div([
                html.Label('The breakdown of events on the topics of sources(all topics events)'),
                dcc.Graph(
                id = 'pie-visits',
                style = {'height': '25vw'}
                )
            ], className = 'six columns'),
            
            html.Div([
                html.Label('Depth of interaction:'),
                dcc.Graph(
                id = 'engagement-graph',
                style = {'height': '25vw'}
                )
            ], className = 'six columns')
        ], className = 'row')
        
        
        
], className = 'row')
# описываем логику дашборда

@app.callback(
        [Output('history-absolute-visits', 'figure'),
        Output('pie-visits', 'figure'),
        Output('engagement-graph', 'figure')
        ],
        [Input('item-topic-dropdown', 'value'),
        Input('age-dropdown', 'value'),
        Input('dt_selector', 'start_date'),
        Input('dt_selector', 'end_date'),
        ])
    
def update_figures(selected_item_topics,
                   selected_ages,
                   start_date,
                   end_date):
                   
    report = dash_visits[(dash_visits['item_topic'].isin(selected_item_topics)) &\
                         (dash_visits['dt'] >= start_date) & (dash_visits['dt'] <= end_date) &\
                         (dash_visits['age_segment'].isin(selected_ages))]
    
    report = report.groupby(['item_topic', 'dt']).agg({'visits':'sum'}).reset_index()
    abs_areas = []
    for i in report['item_topic'].unique():
        current = report[report['item_topic'] == i]
        abs_areas.append(go.Scatter(x = current['dt'],
                                    y = current['visits'],
                                    mode = 'lines',
                                    stackgroup = 'one',
                                    line = {'width': 1},
                                    name = i)
                        )

    report = dash_visits[(dash_visits['item_topic'].isin(selected_item_topics)) &\
                         (dash_visits['dt'] >= start_date) & (dash_visits['dt'] <= end_date) &\
                         (dash_visits['age_segment'].isin(selected_ages))]

    report = (report.groupby(['source_topic']).agg({'visits':'sum'}).reset_index())

    pie_data = [go.Pie(labels = report['source_topic'],
                       values = report['visits'])]
    
    report = dash_engagement[(dash_engagement['item_topic'].isin(selected_item_topics)) &\
                         (dash_engagement['dt'] >= start_date) & (dash_engagement['dt'] <= end_date) &\
                         (dash_engagement['age_segment'].isin(selected_ages))]
    
    report = (report.groupby(['event'])
                    .agg({'unique_users':'mean'})
                    .rename(columns = {'unique_users':'avg_unique_users'})
                    .sort_values(by = 'avg_unique_users', ascending = False)
                    .reset_index())
    
    report['avg_unique_users'] = (report['avg_unique_users'] / report['avg_unique_users'].max()).round(2)
    
    engagement_bars = [go.Bar(x = report['event'],
                              y = report['avg_unique_users'])]
    
    return (
            {
                'data': abs_areas,
                'layout': go.Layout(
                    xaxis = {'title': 'Date & time'},
                    yaxis = {'title': 'Visits'},
                    hovermode = 'closest')
            },
            {
                'data': pie_data,
                
            },
            {
                'data': engagement_bars,
                'layout': go.Layout(
                    xaxis = {'title': 'Funnel stage'},
                    yaxis = {'title': '% of impressions'},
                    hovermode = 'closest')
            },
    
        )


if __name__ == '__main__':
	app.run_server(debug = True, host='0.0.0.0')