#!/usr/bin/env python
# coding: utf-8

# In[9]:


import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
import re
import random
from jupyter_dash import JupyterDash
from dash import Dash, dcc, html, Input, Output


# In[ ]:


dframe = pd.read_excel('C:\\Users\\ArinaBelozerova\\OneDrive - Unwired Ventures Limited\\Desktop\\Occupancy Study Sheet Test (Schroders Data).xlsx', sheet_name = 'Desks')

dframe_meeting = pd.read_excel('C:\\Users\\ArinaBelozerova\\OneDrive - Unwired Ventures Limited\\Desktop\\Occupancy Study Sheet Test (Schroders Data).xlsx', sheet_name = 'Meeting Spaces')


# In[ ]:


#creating relevant columns for further visualizations

dframe['Occupied'] = np.where((dframe['E'] != 'E') & ((dframe['D/L/T'] == 'D') | (dframe['D/L/T'] == 'L') | (dframe['D/L/T'] == 'T')), 1, 0)

dframe['Occupancy x Hour'] = dframe.groupby(['Week', 'Day', 'Time'])['Occupied'].transform('sum')

dframe['Occupancy x Hour x Floor'] = dframe.groupby(['Week', 'Day', 'Time','Floor'])['Occupied'].transform('sum')

dframe['Occupancy x Hour x Team'] = dframe.groupby(['Week', 'Day', 'Time','Team'])['Occupied'].transform('sum')

dframe['Occupancy x Floor x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team','Floor'])['Occupied'].transform('sum')

dframe['Occupancy x Building x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Building'])['Occupied'].transform('sum')

dframe['Number of Desks'] = dframe.groupby(['Week','Day','Time'])['Desk'].transform('count')

dframe['Number of Desks x Team'] = dframe.groupby(['Building','Week','Day','Time','Team'])['Desk'].transform('count')

dframe['Number of Desks x Floor'] = dframe.groupby(['Building','Week','Day','Time','Floor'])['Desk'].transform('count')

dframe['Number of Desks x Team x Floor'] = dframe.groupby(['Building','Week','Day','Time','Floor','Team'])['Desk'].transform('count')

dframe['Number of Desks x Building'] = dframe.groupby(['Building','Week','Day','Time'])['Desk'].transform('count')

dframe['Occupied 10-4'] = np.where((dframe['Time'] != '9am') & (dframe['Time'] != '5pm') & (dframe['E'] != 'E') & ((dframe['D/L/T'] == 'D') | (dframe['D/L/T'] == 'L') | (dframe['D/L/T'] == 'T')), 1, 0)

dframe['Occupancy 10-4 x Hour'] = dframe.groupby(['Week', 'Day', 'Time'])['Occupied 10-4'].transform('sum')

dframe['Occupancy 10-4 x Floor x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Floor'])['Occupied 10-4'].transform('sum')

dframe['Occupancy 10-4 x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team'])['Occupied 10-4'].transform('sum')

dframe['Occupancy 10-4 x Floor x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team','Floor'])['Occupied 10-4'].transform('sum')

dframe['Occupancy 10-4 x Building x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Building'])['Occupied 10-4'].transform('sum')

dframe['Utilised'] = np.where((dframe['S'] == 'S') | ((dframe['D/L/T'] == 'D') | (dframe['D/L/T'] == 'L') | (dframe['D/L/T'] == 'T')), 1, 0)

dframe['Utilisation x Hour'] = dframe.groupby(['Week', 'Day', 'Time'])['Utilised'].transform('sum')

dframe['Utilisation x Floor x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Floor'])['Utilised'].transform('sum')

dframe['Utilisation x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team'])['Utilised'].transform('sum')

dframe['Utilisation x Floor x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team','Floor'])['Utilised'].transform('sum')

dframe['Utilisation x Building x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Building'])['Utilised'].transform('sum')

dframe['Utilised 10-4'] = np.where((dframe['Time'] != '9am') & (dframe['Time'] != '5pm') & ((dframe['S'] == 'S') | ((dframe['D/L/T'] == 'D') | (dframe['D/L/T'] == 'L') | (dframe['D/L/T'] == 'T'))), 1, 0)

dframe['Utilisation 10-4 x Hour'] = dframe.groupby(['Week', 'Day', 'Time'])['Utilised 10-4'].transform('sum')

dframe['Utilisation 10-4 x Floor x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Floor'])['Utilised 10-4'].transform('sum')

dframe['Utilisation 10-4 x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team'])['Utilised 10-4'].transform('sum')

dframe['Utilisation 10-4 x Floor x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team','Floor'])['Utilised 10-4'].transform('sum')

dframe['Utilisation 10-4 x Floor x Team x Hour'] = dframe.groupby(['Week', 'Day', 'Time','Team','Floor'])['Utilised 10-4'].transform('sum')

dframe_meeting['Population x Hour'] = dframe_meeting.groupby(['Building', 'Week', 'Day', 'Time'])['#ppl'].transform('sum')

dframe_meeting['Population x Hour 10-4'] = dframe_meeting[((dframe_meeting['Time'] == '10am') | (dframe_meeting['Time'] == '11am') | (dframe_meeting['Time'] == '12am') | (dframe_meeting['Time'] == '1pm') | (dframe_meeting['Time'] == '2pm') | (dframe_meeting['Time'] == '3pm') | (dframe_meeting['Time'] == '4pm'))].groupby(['Building', 'Week', 'Day', 'Time'])['#ppl'].transform('sum')

dframe_meeting['Population x Hour 10-4 x Floor'] = dframe_meeting[((dframe_meeting['Time'] == '10am') | (dframe_meeting['Time'] == '11am') | (dframe_meeting['Time'] == '12am') | (dframe_meeting['Time'] == '1pm') | (dframe_meeting['Time'] == '2pm') | (dframe_meeting['Time'] == '3pm') | (dframe_meeting['Time'] == '4pm'))].groupby(['Building', 'Week', 'Day', 'Time', 'Floor'])['#ppl'].transform('sum')

dframe_meeting['Hours in Use'] = np.where(((dframe_meeting['E'] == '0') | (dframe_meeting['E'] == 0)), 1, 0)

dframe_meeting['Hours in Use x Room'] = dframe_meeting.groupby(['Week', 'Day', 'Time','Building','Name'])['Hours in Use'].transform('sum')

dframe_meeting['Occupancy x Room'] = (dframe_meeting.groupby(['Space ref no.'])['Hours in Use'].transform('sum'))/45

dframe_meeting['Population x Hour x Floor'] = dframe_meeting.groupby(['Floor', 'Week', 'Day', 'Time'])['#ppl'].transform('sum')

dframe_meeting['Number Meeting Spaces x Floor x Type'] = dframe_meeting.groupby(['Building','Week','Day','Time','Floor', 'Type'])['Space ref no.'].transform('count')

dframe_meeting['Population x Hour x Type'] = dframe_meeting.groupby(['Type', 'Week', 'Day', 'Time'])['#ppl'].transform('sum')

dframe_meeting['Number of Meeting Spaces in Use'] = dframe_meeting.groupby (['Building','Week','Day','Time'])['Hours in Use']. transform('sum')

dframe_meeting['Number of Meeting Spaces in Use x Type'] = dframe_meeting.groupby (['Building','Week','Day','Time','Type'])['Hours in Use']. transform('sum')

dframe_meeting['Population x Building'] = dframe_meeting.groupby(['Building'])['#ppl'].transform('sum')

dframe_meeting['Capacity x Building'] = dframe_meeting.groupby(['Building'])['Capacity'].transform('sum')

dframe_meeting['Number of Meeting Rooms'] = dframe_meeting[(dframe_meeting['Type'] == 'Meeting Room')].groupby(['Building','Type'])['Space ref no.'].transform('nunique')

dframe_meeting['Capacity x Building x Type'] = dframe_meeting.groupby(['Building','Type'])['Capacity'].transform('sum')

dframe_meeting['Capacity x Type x Hour'] = dframe_meeting.groupby(['Week', 'Day', 'Time','Type'])['Capacity'].transform('sum')

dframe_meeting['Number of Meeting Rooms x Building x Floor'] = dframe_meeting[(dframe_meeting['Type'] == 'Meeting Room')].groupby(['Building','Floor'])['Space ref no.'].transform('nunique')

dframe_meeting['Number of Meeting Spaces in Use x Floor x Type'] = dframe_meeting.groupby (['Building','Week','Day','Time','Type','Floor'])['Hours in Use']. transform('sum')

dframe_meeting['Population x Hour x Room x Floor'] = dframe_meeting.groupby(['Floor','Name', 'Week', 'Day', 'Time'])['#ppl'].transform('sum')

dframe_meeting['Capacity x Room'] = dframe_meeting.groupby(['Building', 'Floor', 'Name','Type'])['Capacity'].transform('sum')

dframe_meeting['Capacity x Floor x Room'] = dframe_meeting.groupby(['Building', 'Day','Time','Floor', 'Name'])['Capacity'].transform('sum')

dframe_meeting['Population x Time x Floor x Type'] = dframe_meeting.groupby(['Floor','Type', 'Week', 'Day', 'Time'])['#ppl'].transform('sum')

dframe_meeting['Capacity x Time'] = dframe_meeting.groupby(['Building', 'Day','Time','Floor'])['Capacity'].transform('sum')

dframe_meeting['Number of Meeting spaces (Dynamic)'] = dframe_meeting.groupby(['Type'])['Space ref no.'].transform('nunique')

dframe_meeting['Hours in Use x Name'] = dframe_meeting.groupby(['Week', 'Day', 'Time','Building','Name'])['Hours in Use'].transform('sum')

dframe_meeting['Population x Hour x Name x Floor'] = dframe_meeting.groupby(['Floor','Building', 'Week', 'Day', 'Time','Name'])['#ppl'].transform('sum')

dframe_meeting['Capacity x Floor x Name x Floor'] = dframe_meeting.groupby(['Building','Week','Day','Time','Floor','Name'])['Capacity'].transform('sum')

dframe_meeting['Capacity x Space'] = dframe_meeting.groupby(['Week', 'Day','Time','Space ref no.'])['Capacity'].transform('sum')

dframe_meeting['Meeting Room Population'] = dframe_meeting[(dframe_meeting['Type'] == 'Meeting Room')].groupby(['Week','Day','Time'])['#ppl'].transform('sum')

dframe_meeting['Meeting Room Population x Floor'] = dframe_meeting[(dframe_meeting['Type'] == 'Meeting Room')].groupby(['Week','Day','Time','Floor'])['#ppl'].transform('sum')

dframe_meeting['Number of Breakout Spaces'] = dframe_meeting[(dframe_meeting['Type'] == 'Breakout Space')].groupby(['Building'])['Space ref no.'].transform('nunique')

dframe_meeting['Breakout Space Population'] = dframe_meeting[(dframe_meeting['Type'] == 'Breakout Space')].groupby(['Week','Day','Time'])['#ppl'].transform('sum')

dframe_meeting['Breakout Space Population x Floor'] = dframe_meeting[(dframe_meeting['Type'] == 'Breakout Space')].groupby(['Week','Day','Time','Floor'])['#ppl'].transform('sum')

dframe_meeting['#ppl x Floor'] = dframe_meeting.groupby(['Floor'])['#ppl'].transform('sum')

dframe_meeting['Cafe Population'] = dframe_meeting[(dframe_meeting['Type'] == 'Café')].groupby(['Week','Day','Time'])['#ppl'].transform('sum')


# In[ ]:


#population_desks = dframe[['Building','Floor','Team','Week','Day','Time']].dropna().copy()
population_desks = dframe[['Building','Floor','Week','Day','Time']].dropna().copy()

population_desks['Occupancy x Hour x Floor'] = dframe.groupby(['Building','Floor','Week', 'Day', 'Time'])['Occupied'].transform('sum')

population_desks = population_desks.drop_duplicates()

population_desks = population_desks.sort_values(by=['Week'], kind='mergesort').fillna(0)

population_desks['Week'] = population_desks['Week'].astype(int) 
population_desks['Week'] = population_desks['Week'].astype(str)
population_desks['Time'] = population_desks['Time'].astype(str)
population_desks['Day'] = population_desks['Day'].astype(str)

population_desks['Time Slot'] = population_desks['Time'] + ', ' + population_desks['Day'] + ', Week ' + population_desks['Week']
population_desks = population_desks.fillna(0)
population_desks = population_desks[population_desks['Building'] != 0.].dropna(axis=1)
population_desks = population_desks.reset_index(drop = True)
population_desks['Type'] = pd.Series(['Desks' for x in range(len(population_desks.index))])

#repeating the same for meeting population
population_meetings = dframe_meeting[['Building','Floor','Week','Day','Time', '#ppl']].dropna().copy()

population_meetings['Population x Hour x Floor'] = population_meetings.groupby(['Building','Floor','Week', 'Day', 'Time'])['#ppl'].transform('sum')
population_meetings = population_meetings.drop('#ppl', axis=1)
population_meetings = population_meetings.drop_duplicates().fillna(0)

population_meetings['Week'] = population_meetings['Week'].astype(int) 
population_meetings['Week'] = population_meetings['Week'].astype(str)
population_meetings['Time'] = population_meetings['Time'].astype(str)
population_meetings['Day'] = population_meetings['Day'].astype(str)

population_meetings['Time Slot'] = population_meetings['Time'] + ', ' + population_meetings['Day'] + ', Week ' + population_meetings['Week']
population_meetings = population_meetings.fillna(0)
population_meetings = population_meetings[population_meetings['Building'] != 0.].dropna(axis=1)
population_meetings = population_meetings.reset_index(drop = True)
population_meetings['Type'] = pd.Series(['Meeting Spaces' for x in range(len(population_meetings.index))])

total_population = pd.concat([population_desks, population_meetings], axis=0)
total_population = total_population.fillna(0)
day_mapping = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5}
total_population['Day Num'] = total_population['Day'].map(day_mapping)
time_mapping = {'9am': 1, '10am': 2, '11am': 3, '12pm': 4, '1pm': 5, '2pm': 6, '3pm': 7, '4pm': 8, '5pm': 9}
total_population['Time Num'] = total_population['Time'].map(time_mapping)
total_population = total_population.sort_values(by=['Week','Day Num','Time Num'])
total_population['Week 2'] = 'Week ' + total_population['Week']


# In[ ]:


# lists of buildings, floors, departments, weeks, days, times
building_names = dframe.loc[pd.notna(dframe['Building']), 'Building'].unique()
building_names = [building_item for building_item in building_names if building_item != 0]
combined_df = pd.concat([dframe, dframe_meeting])
floor_names = combined_df['Floor'].unique()
floor_names = [name for name in floor_names if name != 0 and not pd.isna(name)]

floors_total = floor_names
weeks = total_population['Week 2'].unique()
days = total_population['Day'].unique()
times = total_population['Time'].unique()


departments = []
# Check if 'Team' column exists in dframe
if 'Team' in dframe.columns:
    departments = dframe['Team'].unique()


# In[ ]:


#formatting times in desks dataframe
dframe = dframe.dropna(subset=['Week'])
dframe['Week'] = dframe['Week'].astype(int) 
dframe['Week'] = dframe['Week'].astype(str)
dframe['Time'] = dframe['Time'].astype(str)
dframe['Day'] = dframe['Day'].astype(str)
dframe['Time Slot'] = dframe['Time'] + ', ' + dframe['Day'] + ', Week ' + dframe['Week']
dframe['Day Num'] = dframe['Day'].map(day_mapping)
dframe['Time Num'] = dframe['Time'].map(time_mapping)
dframe = dframe.sort_values(by=['Week','Day Num','Time Num'])
dframe['Week 2'] = 'Week ' + dframe['Week']


# In[ ]:


#formatting times in meeting spaces dataframe

dframe_meeting['Week'] = dframe_meeting['Week'].apply(lambda x: str(x).rstrip('.0'))
dframe_meeting['Time'] = dframe_meeting['Time'].astype(str)
dframe_meeting['Day'] = dframe_meeting['Day'].astype(str)
dframe_meeting['Time Slot'] = dframe_meeting['Time'] + ', ' + dframe_meeting['Day'] + ', Week ' + dframe_meeting['Week']
dframe_meeting['Day Num'] = dframe_meeting['Day'].map(day_mapping)
dframe_meeting['Time Num'] = dframe_meeting['Time'].map(time_mapping)
dframe_meeting = dframe_meeting.sort_values(by=['Week','Day Num','Time Num'])
dframe_meeting['Week 2'] = 'Week ' + dframe_meeting['Week']


# In[ ]:


app = JupyterDash()



app.layout = html.Div([
    html.H1('Occupancy Study Report', style={'text-align': 'center', 'font-size': '40px'}),
    #html.Div(style={'padding': '10px'}), 
    html.Div(
        id='filters-container',
        style={'text-align': 'left', 'margin-left': '90px'},
        children=[
            html.Div(
            id='filters-header',
            style={
                'display':'flex',
                'align-items':'center',
                'cursor':'pointer'
            },
            children=[            
                html.H3('Filters'),
                html.Span('▼', id='arrow-icon', style={'marginLeft': '20px'}),
            ],
                n_clicks=0
            ),
            html.Div(
            id='filters-content',
            style={'paddingLeft':'20px',
                  'display':'none'},
            children=[
                html.Div(
                    id='building-container',
                    style={'max-width': '200px'},
                    children=[
                        html.H4('Choose Building', style={'margin-bottom': '4px'}),
                        dcc.Dropdown(
                            id='building-dropdown',
                            options=[{'label': 'All', 'value': ''}] + [{'label': building, 'value': building} for building in building_names],
                            value=[],  # Default selection as an empty list
                            multi=True,
                            style={'width': '100%', 'height': '10px'} 
                        ),
                    ],
                    #style={'display': 'inline-block'} 
                ),
                html.Div(style={'padding': '10px'}),
                html.Div(
                    id='floor-container',
                    style={'max-width': '200px'},
                    children=[
                        html.H4('Choose Floor:', style={'margin-bottom': '4px'}),
                        dcc.Dropdown(
                            id='floor-dropdown',
                            options=[{'label': 'All', 'value': ''}] + [{'label': floor, 'value': floor} for floor in floors_total],
                            value=[],  # Default selection as an empty list
                            multi=True,
                            style={'width': '100%', 'height': '10px'}
                        ),
                    ],
                     #style={'display': 'inline-block'}
                        ),
                html.Div(style={'padding': '10px'}),
                html.Div(
                    id='department-container',
                    style={'max-width': '200px', 'display': 'block' if 'Team' in dframe.columns or 'Team' in dframe_meeting.columns else 'none'},
                    children=[
                        html.H4('Choose Department:', style={'margin-bottom': '4px'}),
                        dcc.Dropdown(
                            id='department-dropdown',
                            options=[{'label': 'All', 'value': ''}] + [{'label': department, 'value': department} for department in departments],
                            value=[],  # Default selection as an empty list
                            multi=True,
                            style={'width': '100%', 'height': '10px'}
                        ),
                    ],
                     #style={'display': 'inline-block'}
                        ),
                #html.Div(style={'padding': '10px'}),
                html.Div(
                    id='week-container',
                    style={'max-width': '200px'},
                    children=[
                        html.H4('Choose Week:', style={'margin-bottom': '4px'}),
                        dcc.Dropdown(
                            id="week",
                            options=[{'label': 'All', 'value': ''}] + [{
                                'label': week,
                                'value': week
                            } for week in weeks],
                            value=[],  # Default selection as an empty list
                            multi=True,
                            style={'width': '100%', 'height': '10px'}),
                    ],
                    #style={'display': 'inline-block'}
                        ),
                html.Div(style={'padding': '10px'}),
                html.Div(
                    id='day-container',
                    style={'max-width': '200px'},
                    children=[
                        html.H4('Choose Day:', style={'margin-bottom': '4px'}),
                        dcc.Dropdown(
                            id="day",
                            options=[{'label': 'All', 'value': ''}] + [{
                                'label': day,
                                'value': day
                            } for day in days],
                            value=[],  # Default selection as an empty list
                            multi=True,
                            style={'width': '100%', 'height': '10px'}),
                    ],
                    #style={'display': 'inline-block'}
                        ),
                html.Div(style={'padding': '10px'}),
                html.Div(
                    id='time-container',
                    style={'max-width': '200px'},
                    children=[
                        html.H4('Choose Time:', style={'margin-bottom': '4px'}),
                        dcc.Dropdown(
                            id="time",
                            options=[{'label': 'All', 'value': ''}] + [{
                                'label': time,
                                'value': time
                            } for time in times],
                            value=[],  # Default selection as an empty list
                            multi=True, 
                            style={'width': '100%', 'height': '10px'}),
                            ],
                        #style={'display': 'inline-block'}
                        ),
                ]                
            ),
        ],
    ),

    html.Div(style={'padding': '10px'}),
    html.Div(
    id='chosen-filters-container',
    style={'margin-left': '90px'},
    children=[
        html.H4('Filters applied:'),
        html.P('  Building:'),
        html.P('  Floor:'),
        html.P('  Week:'),
        html.P('  Day:'),
        html.P('  Time:')
        ]
    ),
    
    html.P('**Note: For the best results please view the dashboard on a bigger display (24"+)',
           style={'text-align': 'left', 'margin-left': '90px'}),
        
    html.Div(style={'padding': '15px'}),
    html.H2('Desks Occupancy & Utilisation', style={'text-align': 'center', 'font-size': '25px'}),
###
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(id='graph-output'),
                         style={'height': '50%', 'width': '100%'}),
                ]),

###
    html.Hr(style={'border': '1px solid #ddd'}),
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(
                    id='graph-output-2',),
                    style={'height':'25%', 'width': '25%'} 
            ),
            html.Div(
                dcc.Graph(
                    id='graph-output-3',),
                    style={'height':'25%', 'width': '25%'}
            ),
            html.Div(
                dcc.Graph(
                    id='graph-daily-occ',),
                    style={'height':'25%', 'width': '25%'}
            ),
            html.Div(
                dcc.Graph(
                    id='graph-daily-ut',),
                    style={'height':'25%', 'width': '25%'}
    )
    ]),
    html.Hr(style={'border': '1px solid #ddd'}),
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(
                    id='graph-hourly-occ',),
                    style={'width': '25%'}
            ),
            html.Div(
                dcc.Graph(
                    id='graph-hourly-ut',),
                    style={'width': '25%'}
            ),
            html.Div(
                dcc.Graph(
                    id='graph-desk-distribution',),
                    style={'width': '25%'}
            ),
            html.Div(
                dcc.Graph(
                    id='graph-binned-occ',),
                    style={'width': '25%'}
    )
    ]),
    
    ###
    html.Hr(style={'border': '1px solid #ddd'}),
    html.Div(
    style={'display': 'flex'},
    children=[
        html.Div(
            dcc.Graph(id='graph-activities'),
                     style={'height': '100%', 'width': '50%'}),
        html.Div(
            dcc.Graph(id='graph-gap'),
                     style={'height': '100%', 'width': '50%'}),
            ]),
    ###
    html.Hr(style={'border': '1px solid #ddd'}),
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(id='graph-table1'),
                         style={'width': '50%'}
            ),
            html.Div(
                dcc.Graph(id='graph-table2'),
                         style={'width': '50%'}
            )
            ]),
    ###
    html.Hr(style={'border': '1px solid #ddd'}), 
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(id='table-banded-desk-occ'),
                         style={'width': '50%'}
            ),
            html.Div(
                dcc.Graph(id='table-low-desk-occ'),
                         style={'width': '50%'}
            )
            ]),
    html.Hr(style={'border': '2px solid #ddd'}),
    html.Div(style={'padding': '5px'}),
    html.H2('Meeting Spaces Occupancy & Utilisation', style={'text-align': 'center', 'font-size': '25px'}),    
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(
                    id='graph-number-meeting-rooms',),
                    style={'width': '50%'}
            ),
            html.Div(
                dcc.Graph(
                    id='graph-number-breakout-spaces',),
                    style={'width': '50%'}
    )
    ]),
    ###     
    html.Hr(style={'border': '1px solid #ddd'}),
    html.Div(
    style={'display': 'flex'},
    children=[
        html.Div(
            dcc.Graph(id='graph-spaces-type'),
                     style={'height': '100%', 'width': '50%'}),
        html.Div(
            dcc.Graph(id='graph-meeting-vs-size'),
                     style={'height': '100%', 'width': '50%'}),
            ]),
    
    ###
    html.Hr(style={'border': '1px solid #ddd'}),
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(id='table-meeting-space-popul'),
                         style={'width': '50%'}
            ),
            html.Div(
                dcc.Graph(id='table-meeting-space-use'),
                         style={'width': '50%'}
            )
            ]),
    
    ###
    html.Hr(style={'border': '1px solid #ddd'}),
    html.Div(
        style={'display': 'flex'},
        children=[
            html.Div(
                dcc.Graph(id='table-meeting-room-pop'),
                         style={'width': '50%'}
            ),
            html.Div(
                dcc.Graph(id='table-meeting-space-in-use'),
                         style={'width': '50%'}
            )
            ]),


])


@app.callback(
    Output('filters-content', 'style'),
    Output('arrow-icon', 'style'),
    Input('filters-header', 'n_clicks')
)
def toggle_filters_content(n_clicks):
    if n_clicks % 2 == 1:
        new_style = {'paddingTop': '10px'}
        arrow_style = {'transform': 'rotate(180deg)'}
    else:
        new_style = {'display': 'none'}
        arrow_style = {'transform': 'rotate(0deg)'}
    
    return new_style, arrow_style


@app.callback(
    Output('chosen-filters-container', 'children'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)
def update_chosen_filters(building, floor, department, week, day, time):
    chosen_building = ', '.join(building) if building else 'All'
    chosen_floor = ', '.join(floor) if floor else 'All'
    chosen_department = ', '.join(department) if department else 'All'
    chosen_week = ', '.join(week) if week else 'All'
    chosen_day = ', '.join(day) if day else 'All'
    chosen_time = ', '.join(time) if time else 'All'

    filters_text = [
        html.H4('Scope of the report:'),
        html.P(f'  Building: {chosen_building}'),
        html.P(f'  Floor: {chosen_floor}'),
        html.P(f'  Department: {chosen_department}' if 'Team' in dframe.columns or  'Team' in dframe_meeting.columns else ''),
        html.P(f'  Week: {chosen_week}'),
        html.P(f'  Day: {chosen_day}'),
        html.P(f'  Time: {chosen_time}')
    ]
    
    if 'Team' not in dframe.columns and 'Team' in dframe_meeting.columns:
        filters_text.append(html.P("* Note: 'Department' filter not applied to desks graphs as departments are not present in the desks data."))
    
    if 'Team' not in dframe_meeting.columns and 'Team' in dframe.columns:
        filters_text.append(html.P("* Note: 'Department' filter not applied to meeting spaces graphs as departments are not present in the meeting spaces data."))

    if 'Team' not in dframe.columns and 'Team' in dframe_meeting.columns:
        filters_text.append(html.P("* Note: 'Department' filter not applied to graphs as departments are not present in the data."))    
        
    return filters_text


@app.callback(
    Output('floor-dropdown', 'options'),
    [Input('building-dropdown', 'value')]
)
def update_floor_options(building):
    if len(building) == 1:
        floor_options = [{'label': 'All', 'value': ''}] + [{'label': str(floor), 'value': floor} for floor in floors_total]
        return floor_options  # Return an empty list to clear the dropdown options

    filtered_data = total_population.copy()  # Start with the original data
    filtered_data = filtered_data[filtered_data['Building'].isin(building)]  # Filter by selected buildings
    floor_names = filtered_data['Floor'].dropna().unique()  # Get unique floor names
    sorted_floor_names = sorted(floor_names, key=lambda x: int(re.match(r'(\d+)', x).group(1)))  # Sort floor names numerically
    floor_options = [{'label': 'All', 'value': ''}] + [{'label': str(floor), 'value': floor} for floor in sorted_floor_names]
    return floor_options


@app.callback(
    Output('department-dropdown', 'options'),
    [Input('building-dropdown', 'value'),
    Input('floor-dropdown', 'value')]
)
def update_department_options(building, floor):
    if 'Team' not in dframe.columns and 'Team' not in dframe_meeting.columns:
        return [{'label': 'All', 'value': ''}]  # Return a default value or an empty list
    
    if building is None or len(building) == 0 and floor is None or len(floor) == 0:
         return [{'label': 'All', 'value': ''}] + [{'label': department, 'value': department} for department in departments]
    
    if building is None or len(building) == 0:
        filtered_data = dframe.copy() 
        filtered_data = filtered_data[filtered_data['Floor'].isin(floor)]
        deparment_names = filtered_data['Team'].dropna().unique()  
        deparment_options = [{'label': 'All', 'value': ''}] + [{'label': str(deparment), 'value': deparment} for deparment in deparment_names]
        return deparment_options
    
    if floor is None or len(floor) == 0:
        filtered_data = dframe.copy() 
        filtered_data = filtered_data[filtered_data['Building'].isin(building)]
        deparment_names = filtered_data['Team'].dropna().unique() 
        deparment_options = [{'label': 'All', 'value': ''}] + [{'label': str(deparment), 'value': deparment} for deparment in deparment_names]
        return deparment_options
    
    filtered_data = dframe.copy()  # Start with the original data
    filtered_data = filtered_data[filtered_data['Building'].isin(building)]
    filtered_data = filtered_data[filtered_data['Floor'].isin(floor)]
    deparment_names = filtered_data['Team'].dropna().unique() 
    deparment_options = [{'label': 'All', 'value': ''}] + [{'label': str(deparment), 'value': deparment} for deparment in deparment_names]
    return deparment_options


@app.callback(
    Output('department-dropdown', 'style'),
    Input('department-dropdown', 'value')
)
def update_department_filter_visibility(selected_department):
    if 'Team' not in dframe.columns and 'Team' not in dframe_meeting.columns:
        return {'display': 'none'}  # Hide the department filter
    else:
        return {'display': 'block'}  # Show the department filter
    
@app.callback(
    Output('graph-number-breakout-spaces', 'style'),
    Input('graph-number-breakout-spaces', 'style'),
)    
def update_BS_graph_visibility(style):
    if 'Breakout Space' in dframe_meeting['Type'].unique():
        return {'width': '100%'}
    else:
        return {'display': 'none'}  # Hide the graph when no breakout spaces are found


def filter_dataframe(total_population, building, floor, department, week, day, time):
    filtered_df = total_population.copy()  
        
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
    
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]

    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department] 
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
    
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
    
    popul_no_dept = filtered_df[['Building', 'Floor', 'Week', 'Day', 'Time', 'Occupancy x Hour x Floor',
                                'Time Slot', 'Type', 'Population x Hour x Floor', 'Day Num', 'Time Num', 'Week 2']].copy().drop_duplicates().reset_index()
    new_filtered_df = popul_no_dept[['Time Slot']].copy()
    new_filtered_df['Occupancy x Hour x Floor'] = popul_no_dept.groupby(['Week','Day','Time'])['Occupancy x Hour x Floor'].transform('sum')
    new_filtered_df['Population x Hour x Floor'] = popul_no_dept.groupby(['Week','Day','Time'])['Population x Hour x Floor'].transform('sum')
    new_filtered_df = new_filtered_df.drop_duplicates()
    
    return new_filtered_df


@app.callback(
    Output('graph-output', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)
def update_graph(building, floor, department, week, day, time):
    filtered_data = filter_dataframe(total_population, building, floor, department, week, day, time)
        
    trace_desks_popl = go.Bar(
        x=filtered_data['Time Slot'],
        y=filtered_data['Occupancy x Hour x Floor'],
        name='Desks',
        marker_color='#26A2ED'
    )

    trace_meeting_popl = go.Bar(
        x=filtered_data['Time Slot'],
        y=filtered_data['Population x Hour x Floor'],
        name='Meeting Spaces',
        marker_color='#41C572'
    )
    
    # Adding the line for average population
    overall_avg_occupancy = int(round((filtered_data['Occupancy x Hour x Floor'] + filtered_data['Population x Hour x Floor']).mean()))
    
    avg_occupancy_trace = go.Scatter(
        x=filtered_data['Time Slot'],
        y=[overall_avg_occupancy] * len(filtered_data['Time Slot']),
        name='Average Occupancy',
        mode='lines',
        marker_color = 'Black',
        showlegend=False
    ) 
    
    # Adding the line for maximum population
    overall_max_occupancy = int(round((filtered_data['Occupancy x Hour x Floor'] + filtered_data['Population x Hour x Floor']).max()))
    
    max_occupancy_trace = go.Scatter(
        x=filtered_data['Time Slot'],
        y=[overall_max_occupancy] * len(filtered_data['Time Slot']),
        name='Maximum Occupancy',
        mode='lines',
        line_dash ='dot', marker_color = 'Black',
        showlegend=False
    )    

    # Adding the line for minimum population
    overall_min_occupancy = int(round((filtered_data['Occupancy x Hour x Floor'] + filtered_data['Population x Hour x Floor']).min()))
    
    min_occupancy_trace = go.Scatter(
        x=filtered_data['Time Slot'],
        y=[overall_min_occupancy] * len(filtered_data['Time Slot']),
        name='Minimum Occupancy',
        mode='lines',
        line_dash ='dot', marker_color = 'Black',
        showlegend=False
    )    
    
    
    return {
        'data': [trace_desks_popl, trace_meeting_popl, avg_occupancy_trace, max_occupancy_trace, min_occupancy_trace],
        'layout': go.Layout(
            title='Office Population',
            barmode='stack',
            template="simple_white"
        )
    }

#__________________________________________________________________________________________________________________________
# OCCUPANCY OVERALL

def filter_dataframe_occ(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()  
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
    
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
    
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
    
    new_filtered_df_occ = filtered_df[['Time Slot']].copy()
    new_filtered_df_occ['Occupancy x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Occupied'].transform('sum')
    new_filtered_df_occ['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_occ = new_filtered_df_occ.drop_duplicates() 
    
    return new_filtered_df_occ

def filter_dataframe_occ_10_4(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()  
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
    
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]

    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
    
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
                
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
                
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
    new_filtered_df_occ_10_4 = filtered_df[['Time Slot']].copy()
    new_filtered_df_occ_10_4['Occupancy 10-4 x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Occupied 10-4'].transform('sum')
    new_filtered_df_occ_10_4['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_occ_10_4 = new_filtered_df_occ_10_4.drop_duplicates()
    new_filtered_df_occ_10_4 = new_filtered_df_occ_10_4[new_filtered_df_occ_10_4['Occupancy 10-4 x Hour'] != 0]
        
    return new_filtered_df_occ_10_4


@app.callback(
    Output('graph-output-2', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_2(building, floor, department, week, day, time):
    filtered_data_occ = filter_dataframe_occ(dframe, building, floor, department, week, day, time)
    filtered_data_occ_10_4 = filter_dataframe_occ_10_4(dframe, building, floor, department, week, day, time)
      
    min_occupancy = round(filtered_data_occ['Occupancy x Hour'].min()/filtered_data_occ['Number of Desks'].max(),2)
    max_occupancy = round(filtered_data_occ['Occupancy x Hour'].max()/filtered_data_occ['Number of Desks'].max(),2)
    mean_occupancy = round(filtered_data_occ['Occupancy x Hour'].mean()/filtered_data_occ['Number of Desks'].max(),2)
    mean10_4_occupancy = round(filtered_data_occ_10_4['Occupancy 10-4 x Hour'].mean()/filtered_data_occ_10_4['Number of Desks'].max(),2)
    
    occupancy_colours = ["#26a2ed","#41c572","#f05050","#f4d646"]
    
    occupancy_data= {"Occupancy":[min_occupancy,mean_occupancy,max_occupancy,mean10_4_occupancy],
       "Statistics":["Minimum","Average","Maximum","Maximum Average"]
}

    trace_occupancy = go.Bar(x=occupancy_data["Statistics"],
                                y=(occupancy_data["Occupancy"]), 
                                text=(occupancy_data["Occupancy"]),
                                textposition="outside",
                                texttemplate="%{y:.0%}",
                                marker_color=occupancy_colours,
                                width=[1,1,1,1])

    return {
        'data': [trace_occupancy],
        'layout': go.Layout(
            yaxis_range=[0,1],
            yaxis_tickformat = ".0%",
            yaxis_dtick=0.2,
            yaxis_title_text="Occupancy as a Percentage of Total Desks",
            template="simple_white",
            title_text="Overall Desk Occupancy"
        )
    }

#__________________________________________________________________________________________________________________________________________
# UTILISATION OVERALL 

def filter_dataframe_ut(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()    
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
    
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
    
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    new_filtered_df_ut = filtered_df[['Time Slot']].copy()
    new_filtered_df_ut['Utilisation x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Utilised'].transform('sum')
    new_filtered_df_ut['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_ut = new_filtered_df_ut.drop_duplicates()
        
    return new_filtered_df_ut

def filter_dataframe_ut_10_4(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()  
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
            
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
            
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
            
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day] 
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
                
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
    new_filtered_df_ut_10_4 = filtered_df[['Time Slot']].copy()
    new_filtered_df_ut_10_4['Utilisation 10-4 x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Utilised 10-4'].transform('sum')
    new_filtered_df_ut_10_4['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_ut_10_4 = new_filtered_df_ut_10_4.drop_duplicates()
    new_filtered_df_ut_10_4 = new_filtered_df_ut_10_4[new_filtered_df_ut_10_4['Utilisation 10-4 x Hour'] != 0]
        
    return new_filtered_df_ut_10_4


@app.callback(
    Output('graph-output-3', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)
def update_graph_3(building, floor, department, week, day, time):
    filtered_data_ut = filter_dataframe_ut(dframe, building, floor, department, week, day, time)
    filtered_data_ut_10_4 = filter_dataframe_ut_10_4(dframe, building, floor, department, week, day, time)
      
    min_utilisation = round(filtered_data_ut['Utilisation x Hour'].min()/filtered_data_ut['Number of Desks'].max(),2)
    max_utilisation = round(filtered_data_ut['Utilisation x Hour'].max()/filtered_data_ut['Number of Desks'].max(),2)
    mean_utilisation = round(filtered_data_ut['Utilisation x Hour'].mean()/filtered_data_ut['Number of Desks'].max(),2)
    mean10_4_utilisation = round(filtered_data_ut_10_4['Utilisation 10-4 x Hour'].mean()/filtered_data_ut_10_4['Number of Desks'].max(),2)
    
    utilisation_colours = ["#26a2ed","#41c572","#f05050","#f4d646"]

    utilisation_data= {"Utilisation":[min_utilisation,mean_utilisation,max_utilisation,mean10_4_utilisation],
       "Statistics":["Minimum","Average","Maximum","Maximum Average"]
}

    trace_utilisation = go.Bar(x=utilisation_data["Statistics"],
                                y=(utilisation_data["Utilisation"]), 
                                text=(utilisation_data["Utilisation"]),
                                textposition="outside",
                                texttemplate="%{y:.0%}",
                                marker_color=utilisation_colours,
                                width=[1,1,1,1])

    return {
        'data': [trace_utilisation],
        'layout': go.Layout(
            yaxis_range=[0,1],
            yaxis_tickformat = ".0%",
            yaxis_dtick=0.2,
            yaxis_title_text="Utilisation as a Percentage of Total Desks",
            template="simple_white",
            title_text="Overall Desk Utilisation"
        )
    }



#___________________________________________________________________________________________________________________
#OCCUPANCY BY DAY

def filter_dataframe_daily_occ(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()    
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
            
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
   
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
    
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
          
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    new_filtered_df_daily_occ = filtered_df[['Time Slot', 'Day']].copy()
    new_filtered_df_daily_occ['Occupancy x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Occupied'].transform('sum')
    new_filtered_df_daily_occ['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_daily_occ = new_filtered_df_daily_occ.drop_duplicates()

    new_filtered_df_daily_occ_10_4 = filtered_df[['Time Slot','Day']].copy()
    new_filtered_df_daily_occ_10_4['Occupancy 10-4 x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Occupied 10-4'].transform('sum')
    new_filtered_df_daily_occ_10_4['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_daily_occ_10_4 = new_filtered_df_daily_occ_10_4.drop_duplicates()
    new_filtered_df_daily_occ_10_4 = new_filtered_df_daily_occ_10_4[new_filtered_df_daily_occ_10_4['Occupancy 10-4 x Hour'] != 0]
    
    return new_filtered_df_daily_occ, new_filtered_df_daily_occ_10_4


color_map = {
    "Minimum": "#26a2ed",
    "Average": "#41c572",
    "Maximum": "#f05050",
    "Maximum Average": "#f4d646"
}

@app.callback(
    Output('graph-daily-occ', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)
def update_graph_daily_occ(building, floor, department, week, day, time):
    filtered_data_daily_occ, filtered_data_daily_occ_10_4 = filter_dataframe_daily_occ(dframe, building, floor, department, week, day, time)

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    traces = []

    for occupancy_type in ['Minimum', 'Average', 'Maximum', 'Maximum Average']:
        y_values = []
        for day in days_of_week:
            data_occ_day = filtered_data_daily_occ[filtered_data_daily_occ['Day'] == day]
            min_occ = round(data_occ_day['Occupancy x Hour'].min() / filtered_data_daily_occ['Number of Desks'].max(), 4)
            mean_occ = round(data_occ_day['Occupancy x Hour'].mean() / filtered_data_daily_occ['Number of Desks'].max(), 4)
            max_occ = round(data_occ_day['Occupancy x Hour'].max() / filtered_data_daily_occ['Number of Desks'].max(), 2)
            data_occ_day_10_4 = filtered_data_daily_occ_10_4[filtered_data_daily_occ_10_4['Day'] == day]
            mean10_4_occ = round(data_occ_day_10_4['Occupancy 10-4 x Hour'].mean() / filtered_data_daily_occ['Number of Desks'].max(), 2)

            occupancy_data = {
                'Minimum': min_occ,
                'Average': mean_occ,
                'Maximum': max_occ,
                'Maximum Average': mean10_4_occ
            }
            y_values.append(occupancy_data[occupancy_type])
        
        trace = go.Bar(
            name=occupancy_type,
            x=days_of_week,
            y=y_values,
            marker_color=color_map[occupancy_type]
        )
        traces.append(trace)
    
    layout = go.Layout(
        barmode='group',
        template="simple_white",
        yaxis_range=[0, 1],
        yaxis_dtick=0.2,
        yaxis_tickformat=".0%",
        title_text="Occupancy by Day",
        bargap=0.2,
        showlegend = False,
    )

    return {'data': traces, 'layout': layout}   


#___________________________________________________________________________________________________________________
#UTILISATION BY DAY

def filter_dataframe_daily_ut(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()  
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
         
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]

    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]

    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
    
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    new_filtered_df_daily_ut = filtered_df[['Time Slot', 'Day']].copy()
    new_filtered_df_daily_ut['Utilisation x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Utilised'].transform('sum')
    new_filtered_df_daily_ut['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_daily_ut = new_filtered_df_daily_ut.drop_duplicates()

    new_filtered_df_daily_ut_10_4 = filtered_df[['Time Slot','Day']].copy()
    new_filtered_df_daily_ut_10_4['Utilisation 10-4 x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Utilised 10-4'].transform('sum')
    new_filtered_df_daily_ut_10_4['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_daily_ut_10_4 = new_filtered_df_daily_ut_10_4.drop_duplicates()
    new_filtered_df_daily_ut_10_4 = new_filtered_df_daily_ut_10_4[new_filtered_df_daily_ut_10_4['Utilisation 10-4 x Hour'] != 0]

    return new_filtered_df_daily_ut, new_filtered_df_daily_ut_10_4

@app.callback(
    Output('graph-daily-ut', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)
def update_graph_daily_ut(building, floor, department, week, day, time):
    filtered_data_daily_ut, filtered_data_daily_ut_10_4 = filter_dataframe_daily_ut(dframe, building, floor, department, week, day, time)

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    traces = []

    for utilisation_type in ['Minimum', 'Average', 'Maximum', 'Maximum Average']:
        y_values = []
        for day in days_of_week:
            data_ut_day = filtered_data_daily_ut[filtered_data_daily_ut['Day'] == day]
            min_ut = round(data_ut_day['Utilisation x Hour'].min() / filtered_data_daily_ut['Number of Desks'].max(), 4)
            mean_ut = round(data_ut_day['Utilisation x Hour'].mean() / filtered_data_daily_ut['Number of Desks'].max(), 4)
            max_ut = round(data_ut_day['Utilisation x Hour'].max() / filtered_data_daily_ut['Number of Desks'].max(), 2)
            data_ut_day_10_4 = filtered_data_daily_ut_10_4[filtered_data_daily_ut_10_4['Day'] == day]
            mean10_4_ut = round(data_ut_day_10_4['Utilisation 10-4 x Hour'].mean() / filtered_data_daily_ut['Number of Desks'].max(), 2)

            utilisation_data = {
                'Minimum': min_ut,
                'Average': mean_ut,
                'Maximum': max_ut,
                'Maximum Average': mean10_4_ut
            }
            y_values.append(utilisation_data[utilisation_type])
        
        trace = go.Bar(
            name=utilisation_type,
            x=days_of_week,
            y=y_values,
            marker_color=color_map[utilisation_type]
        )
        traces.append(trace)
    
    layout = go.Layout(
        barmode='group',
        template="simple_white",
        yaxis_range=[0, 1],
        yaxis_dtick=0.2,
        yaxis_tickformat=".0%",
        title_text="Utilisation by Day",
        bargap=0.2,
    )

    return {'data': traces, 'layout': layout}   


#_________________________________________________________________________________________________________________________________________
# HOURLY OCCUPANCY

def filter_dataframe_hourly_occ(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy() 
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
           
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
   
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department] 
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
         
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
    
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
          
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  # Convert to list if a single time is selected
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    new_filtered_df_hourly_occ = filtered_df[['Time Slot', 'Time']].copy()
    new_filtered_df_hourly_occ['Occupancy x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Occupied'].transform('sum')
    new_filtered_df_hourly_occ['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_hourly_occ = new_filtered_df_hourly_occ.drop_duplicates()
    
    return new_filtered_df_hourly_occ

@app.callback(
    Output('graph-hourly-occ', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_hourly_occ(building, floor, department, week, day, time):
    filtered_data_hourly_occ = filter_dataframe_hourly_occ(dframe, building, floor, department, week, day, time)
    
    time_slots = ['9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm']
    
    data_by_time = {}
    for slot in time_slots:
        data_by_time[slot] = filtered_data_hourly_occ[filtered_data_hourly_occ['Time'] == slot]
        
    calculated_values = {}
    for slot, data in data_by_time.items():
        min_occ = round(data['Occupancy x Hour'].min() / filtered_data_hourly_occ['Number of Desks'].max(), 4)
        max_occ = round(data['Occupancy x Hour'].max() / filtered_data_hourly_occ['Number of Desks'].max(), 2)
        mean_occ = round(data['Occupancy x Hour'].mean() / filtered_data_hourly_occ['Number of Desks'].max(), 4)
        error_occ = (max_occ - min_occ) / 2
        calculated_values[slot] = (mean_occ, error_occ)
    
    x_data_hourly_occ = time_slots
    y_data_hourly_occ = [values[0] for values in calculated_values.values()]
    error_data_hourly_occ = [values[1] for values in calculated_values.values()]

    trace_hourly_occ = go.Scatter(
        x=x_data_hourly_occ,
        y=y_data_hourly_occ,
        line=dict(color='#5dcd87'),
        error_y=dict(
            type='data',
            array=error_data_hourly_occ,
            color='#8e8e8e',
            visible=True)
    )

    return {
        'data': [trace_hourly_occ],
        'layout': go.Layout(
            yaxis_range=[0, 1],
            yaxis_tickformat=".0%",
            template="simple_white",
            xaxis=dict(title_text="Time"),
            yaxis=dict(title_text="Average Occupancy"),
            title_text="Occupancy by Hour",
            yaxis_dtick=0.2)
    }


#_________________________________________________________________________________________________________________________________________
# HOURLY UTILITSATION

def filter_dataframe_hourly_ut(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
           
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
   
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
         
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
          
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    new_filtered_df_hourly_ut = filtered_df[['Time Slot', 'Time']].copy()
    new_filtered_df_hourly_ut['Utilisation x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Utilised'].transform('sum')
    new_filtered_df_hourly_ut['Number of Desks'] = filtered_df.groupby(['Week','Day','Time'])['Desk'].transform('count')
    new_filtered_df_hourly_ut = new_filtered_df_hourly_ut.drop_duplicates()
    
    return new_filtered_df_hourly_ut

@app.callback(
    Output('graph-hourly-ut', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_hourly_ut(building, floor, department, week, day, time):
    filtered_data_hourly_ut = filter_dataframe_hourly_ut(dframe, building, floor, department, week, day, time)
    
    time_slots = ['9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm']
    
    data_by_time = {}
    for slot in time_slots:
        data_by_time[slot] = filtered_data_hourly_ut[filtered_data_hourly_ut['Time'] == slot]
        
    calculated_values = {}
    for slot, data in data_by_time.items():
        min_ut = round(data['Utilisation x Hour'].min() / filtered_data_hourly_ut['Number of Desks'].max(), 4)
        max_ut = round(data['Utilisation x Hour'].max() / filtered_data_hourly_ut['Number of Desks'].max(), 2)
        mean_ut = round(data['Utilisation x Hour'].mean() / filtered_data_hourly_ut['Number of Desks'].max(), 4)
        error_ut = (max_ut - min_ut) / 2
        calculated_values[slot] = (mean_ut, error_ut)
    
    x_data_hourly_ut = time_slots
    y_data_hourly_ut = [values[0] for values in calculated_values.values()]
    error_data_hourly_ut = [values[1] for values in calculated_values.values()]

    trace_hourly_ut = go.Scatter(
        x=x_data_hourly_ut,
        y=y_data_hourly_ut,
        line=dict(color='#5dcd87'),
        error_y=dict(
            type='data',
            array=error_data_hourly_ut,
            color='#8e8e8e',
            visible=True)
    )

    return {
        'data': [trace_hourly_ut],
        'layout': go.Layout(
            yaxis_range=[0, 1],
            yaxis_tickformat=".0%",
            template="simple_white",
            xaxis=dict(title_text="Time"),
            yaxis=dict(title_text="Average Occupancy"),
            title_text="Utilisation by Hour",
            yaxis_dtick=0.2)
    }


#_________________________________________________________________________________________________________________________________________________________________
#DESKS DISTRIBUTION

def filter_dataframe_distribution(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()  
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
                   
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
 
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
                 
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
          
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time] 
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    new_filtered_df_distribution = filtered_df[['Desk ref no.']].copy()
    new_filtered_df_distribution['Times Desk Occupied'] = dframe.groupby(['Desk ref no.'])['Occupied'].transform('sum')
    new_filtered_df_distribution = new_filtered_df_distribution.drop_duplicates()

    new_filtered_df_distribution['Occupancy Percentage'] = round(new_filtered_df_distribution['Times Desk Occupied']/90,2)

    bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1,] 
    group_names= list([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95])
    new_filtered_df_distribution["Occupancy Bin"] = pd.cut(new_filtered_df_distribution['Occupancy Percentage'], bins, labels=group_names)

    new_filtered_df_distribution['N of Desks in Bins'] = new_filtered_df_distribution.groupby(['Occupancy Bin'])['Occupancy Bin'].transform('count')
    new_filtered_df_distribution['Desk Pecentage'] = round(new_filtered_df_distribution['N of Desks in Bins']/new_filtered_df_distribution['Desk ref no.'].count(),3)

    final_filtered_df_distribution = new_filtered_df_distribution[['Occupancy Bin','Desk Pecentage']].drop_duplicates().dropna()
    
    return new_filtered_df_distribution, final_filtered_df_distribution


@app.callback(
    Output('graph-desk-distribution', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_distribution(building, floor, department, week, day, time):
    new_filtered_df_distribution, filtered_data_distribution = filter_dataframe_distribution(dframe, building, floor, department, week, day, time)
    filtered_data_distribution = filtered_data_distribution.sort_values(by='Occupancy Bin')
    
    trace_distribution = go.Bar(
        x=filtered_data_distribution['Occupancy Bin'],
        y=filtered_data_distribution['Desk Pecentage'], 
        marker_color=['#26A2ED'] * len(filtered_data_distribution),
        showlegend=False
                            )
    
    desks_distr_mean = new_filtered_df_distribution['Occupancy Percentage'].mean()
    
    avg_distr_trace = go.Scatter(
                            x = [desks_distr_mean, desks_distr_mean], 
                            y = [0, filtered_data_distribution['Desk Pecentage'].max()], 
                            mode= 'lines', 
                            marker_color = 'Black', 
                            line=dict(width=1.5),
                            showlegend=False
    )    
    
    desks_distr_minus_sd = (new_filtered_df_distribution['Occupancy Percentage'].mean()-np.std(new_filtered_df_distribution['Occupancy Percentage']))

    minus_sd_distr_trace = go.Scatter(
                            x = [desks_distr_minus_sd, desks_distr_minus_sd], 
                            y = [0, filtered_data_distribution['Desk Pecentage'].max()], 
                            mode= 'lines', 
                            marker_color = 'Black', 
                            line_dash ='dash',
                            line=dict(width=1.5),
                            showlegend=False
    )   
    
    desks_distr_plus_sd = (new_filtered_df_distribution['Occupancy Percentage'].mean()+np.std(new_filtered_df_distribution['Occupancy Percentage']))

    plus_sd_distr_trace = go.Scatter(
                            x = [desks_distr_plus_sd, desks_distr_plus_sd], 
                            y = [0, filtered_data_distribution['Desk Pecentage'].max()], 
                            mode= 'lines', 
                            marker_color = 'Black', 
                            line_dash ='dash',
                            line=dict(width=1.5),
                            showlegend=False
    )   
        
        
    return {
        'data': [trace_distribution, avg_distr_trace, minus_sd_distr_trace, plus_sd_distr_trace],
        'layout': go.Layout(bargap=0.001,
                            template='simple_white',
                            yaxis_tickformat = ".0%",
                            xaxis_tickformat = ".0%",
                            xaxis_title = 'Average Level of Desk Occupancy',
                            yaxis_title = 'Percentage of Desks',
                            title_text='Distribution of Desk Occupancy Levels',
                            xaxis_range=[0,1],
                            yaxis_dtick=0.1,
                            xaxis_dtick=0.1)
    }



#_________________________________________________________________________________________________________________________________________________________________
#BINNED OCCUPANCY

def filter_dataframe_binned_occ(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()  
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
                   
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department] 
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
                
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    new_filtered_df_distribution = filtered_df[['Time','Day','Week','Occupancy x Hour']].copy().dropna()
    new_filtered_df_distribution = new_filtered_df_distribution.drop_duplicates()
    new_filtered_df_distribution['Occupancy x Hour'] = new_filtered_df_distribution['Occupancy x Hour'].astype(int)

    #creating bins    
    desk_occ_bins = np.arange(0,new_filtered_df_distribution['Occupancy x Hour'].max() + 20, 20)
    desk_occ_labels = ['-'.join(map(str,(x,y))) for x, y in zip(desk_occ_bins[:-1], desk_occ_bins[1:])]
    new_filtered_df_distribution['Occupancy Bins'] = pd.cut(new_filtered_df_distribution['Occupancy x Hour'], bins = desk_occ_bins, labels=desk_occ_labels)   
    new_filtered_df_distribution["Unique Count Occupancy Bin"] = new_filtered_df_distribution.groupby(['Occupancy Bins'])['Occupancy Bins'].transform('count')


    #new dataframe with columns for histogram
    final_filtered_df_distribution = new_filtered_df_distribution[['Occupancy Bins',"Unique Count Occupancy Bin"]].drop_duplicates()
    final_filtered_df_distribution = final_filtered_df_distribution.sort_values(by = 'Occupancy Bins')
    final_filtered_df_distribution['Occupancy Bins'] = final_filtered_df_distribution['Occupancy Bins'].astype('str')

    #changing occupancy bins from string to integer and finding mean value between two
    final_filtered_df_distribution['Final Occupancy Bins'] = new_filtered_df_distribution['Occupancy Bins'].str.split("-")
    final_filtered_df_distribution['Floor2'] = final_filtered_df_distribution['Occupancy Bins'].str.extract('(\d+)')
    final_filtered_df_distribution['Floor3'] = final_filtered_df_distribution['Occupancy Bins'].str[::-1].str.extract('(\d+)')
    final_filtered_df_distribution['Floor3'] = final_filtered_df_distribution['Floor3'].str[::-1]
    final_filtered_df_distribution['Floor2'] = final_filtered_df_distribution['Floor2'].astype(float)
    final_filtered_df_distribution['Floor3'] = final_filtered_df_distribution['Floor3'].astype(float)
    final_filtered_df_distribution['Finalle Occupancy Bins'] = (final_filtered_df_distribution['Floor2'] + final_filtered_df_distribution['Floor3'])/2
    final_filtered_df_distribution = final_filtered_df_distribution.reset_index(drop = True)
        
    return final_filtered_df_distribution


@app.callback(
    Output('graph-binned-occ', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_distribution(building, floor, department, week, day, time):
    filtered_data_distribution = filter_dataframe_binned_occ(dframe, building, floor, department, week, day, time)
    
    trace_distribution = go.Bar(
        x=filtered_data_distribution['Finalle Occupancy Bins'],
        y=filtered_data_distribution['Unique Count Occupancy Bin'], 
        marker_color=['#26A2ED'] * len(filtered_data_distribution))
            
        
    return {
        'data': [trace_distribution],
        'layout': go.Layout(bargap=0.001,
                            template='simple_white',
                            xaxis_title = 'Occupancy',
                            yaxis_title = 'Number of Observations',
                            title_text='Binned Desk Occupancy by Number of Observations',
                            xaxis_dtick=20)
                           
    }


#_________________________________________________________________________________________________________________________________________________________________
#DESK ACTIVITIES

def filter_dataframe_activities(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy() 
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
        
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
                
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  # Convert to list if a single time is selected
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    df_desks_usage_activities = filtered_df[['Week','Day','Time','E','D/L/T','P', 'S', 'At desk meeting']].dropna()
    df_desks_usage_activities['Desktop'] = np.where(((df_desks_usage_activities['D/L/T'] == 'D') & (df_desks_usage_activities['E'] != 'E')), 1, 0)
    df_desks_usage_activities['Laptop'] = np.where((df_desks_usage_activities['D/L/T'] == 'L'), 1, 0)
    df_desks_usage_activities['Tablet'] = np.where((df_desks_usage_activities['D/L/T'] == 'T'), 1, 0)
    df_desks_usage_activities['Signs of Life'] = np.where(((df_desks_usage_activities['S'] == 'S')), 1, 0)
    df_desks_usage_activities['Phone'] = np.where((df_desks_usage_activities['P'] == 'P'), 1, 0)
    df_desks_usage_activities['Meeting'] = np.where((df_desks_usage_activities['At desk meeting'] != 0), 1, 0)
    df_desks_usage_activities = df_desks_usage_activities.sort_values(by=['Week'], kind='mergesort')
    df_desks_usage_activities['Week'] = df_desks_usage_activities['Week'].astype(int)
    df_desks_usage_activities['Week'] = df_desks_usage_activities['Week'].astype(str)
    df_desks_usage_activities['Time Slot'] = df_desks_usage_activities['Time'] + ', ' + df_desks_usage_activities['Day'] + ', Week ' + df_desks_usage_activities['Week']

    df_desks_usage_activities['Number Desktop x Hour'] = df_desks_usage_activities.groupby(['Week', 'Day', 'Time'])['Desktop'].transform('sum')
    df_desks_usage_activities['Number Laptop x Hour'] = df_desks_usage_activities.groupby(['Week', 'Day', 'Time'])['Laptop'].transform('sum')
    df_desks_usage_activities['Number Tablet x Hour'] = df_desks_usage_activities.groupby(['Week', 'Day', 'Time'])['Tablet'].transform('sum')
    df_desks_usage_activities['Number Phone x Hour'] = df_desks_usage_activities.groupby(['Week', 'Day', 'Time'])['Phone'].transform('sum')
    df_desks_usage_activities['Number Recent Users x Hour'] = df_desks_usage_activities.groupby(['Week', 'Day', 'Time'])['Signs of Life'].transform('sum')
    df_desks_usage_activities['Number At Desk Meeting x Hour'] = df_desks_usage_activities.groupby(['Week', 'Day', 'Time'])['Meeting'].transform('sum')
    df_desks_usage_activities = df_desks_usage_activities.copy()

    df_desks_usage_activities_final = df_desks_usage_activities[['Time Slot', 'Number Desktop x Hour', 
                                                                'Number Laptop x Hour',
                                                                'Number Tablet x Hour', 'Number Phone x Hour',
                                                                'Number Recent Users x Hour', 'Number At Desk Meeting x Hour'
                                                                ]]
    df_desks_usage_activities_final = df_desks_usage_activities_final.drop_duplicates() 
        
    return df_desks_usage_activities_final


@app.callback(
    Output('graph-activities', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_activities(building, floor, department, week, day, time):
    filtered_data_activities = filter_dataframe_activities(dframe, building, floor, department, week, day, time)
    
    activity_types = [
        ('Desktop Equipment', '#26A2ED', 'Number Desktop x Hour'),
        ('At-Desk Meeting', '#41C572', 'Number At Desk Meeting x Hour'),
        ('Tablet', '#F05050', 'Number Tablet x Hour'),
        ('Laptop', '#F4D646', 'Number Laptop x Hour'),
        ('Phone Use', '#b2a1e2', 'Number Phone x Hour'),
        ('Recently Occupied Desks', '#F99B15', 'Number Recent Users x Hour')
        ]

    traces = []

    for activity_name, color, data_column in activity_types:
        trace = go.Bar(
            x=filtered_data_activities['Time Slot'],
            y=filtered_data_activities[data_column],
            name=activity_name,
            marker_color=color
        )
        traces.append(trace)      
        
    activities_max = (filtered_data_activities['Number Desktop x Hour'] 
                                     + filtered_data_activities['Number At Desk Meeting x Hour'] 
                                     + filtered_data_activities['Number Tablet x Hour'] 
                                     + filtered_data_activities['Number Laptop x Hour'] 
                                     + filtered_data_activities['Number Phone x Hour'] 
                                     + filtered_data_activities['Number Recent Users x Hour']).max()
    activities_mean = round((filtered_data_activities['Number Desktop x Hour'] 
                                            + filtered_data_activities['Number At Desk Meeting x Hour'] 
                                            + filtered_data_activities['Number Tablet x Hour'] 
                                            + filtered_data_activities['Number Laptop x Hour'] 
                                            + filtered_data_activities['Number Phone x Hour'] 
                                            + filtered_data_activities['Number Recent Users x Hour']).mean())
    activities_min = (filtered_data_activities['Number Desktop x Hour'] 
                                     + filtered_data_activities['Number At Desk Meeting x Hour'] 
                                     + filtered_data_activities['Number Tablet x Hour'] 
                                     + filtered_data_activities['Number Laptop x Hour'] 
                                     + filtered_data_activities['Number Phone x Hour'] 
                                     + filtered_data_activities['Number Recent Users x Hour']).min()

    min_trace = go.Scatter(
        x=filtered_data_activities['Time Slot'],
        y=[activities_min] * len(filtered_data_activities['Time Slot']),
        name = 'Minimum',
        mode='lines',
        line_dash ='dot', marker_color = 'Black',
        showlegend=False
    )   
    
    mean_trace = go.Scatter(
        x=filtered_data_activities['Time Slot'],
        y=[activities_mean] * len(filtered_data_activities['Time Slot']),
        name = 'Average',
        mode='lines',
        line_dash ='dot', marker_color = 'Black',
        showlegend=False
    )   
       
    max_trace = go.Scatter(
        x=filtered_data_activities['Time Slot'],
        y=[activities_max] * len(filtered_data_activities['Time Slot']),
        name = 'Maximum',
        mode='lines',
        line_dash ='dot', marker_color = 'Black',
        showlegend=False
    )   
    
    traces.append(min_trace)
    traces.append(mean_trace)
    traces.append(max_trace)
       
    return {
        'data': traces, 
        'layout': go.Layout(barmode= 'stack',
                            title='Desk Activities',
                            xaxis=dict(title='Time'),
                            yaxis=dict(title='Number of People'),
                            template="simple_white",
                            bargap=0.03)
                           
    }


#_________________________________________________________________________________________________________________________________________________________________
#OCCUPANCY/UTILISATION GAP

def filter_dataframe_gap(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
           
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]

    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
            
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  # Convert to list if a single time is selected
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    df_estate_desks = filtered_df[['Week','Day','Time','Occupancy x Hour','Utilisation x Hour','Number of Desks']].dropna().copy()

    df_estate_desks = df_estate_desks.drop_duplicates()
    df_estate_desks = df_estate_desks.reset_index()

    df_estate_desks['Week'] = df_estate_desks['Week'].astype(int) 
    df_estate_desks['Week'] = df_estate_desks['Week'].astype(str)
    df_estate_desks['Time Slot'] = df_estate_desks['Time'] + ', ' + df_estate_desks['Day'] + ', Week ' + df_estate_desks['Week'] 
        
    return df_estate_desks


@app.callback(
    Output('graph-gap', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_gap(building, floor, department, week, day, time):
    filtered_data_distribution = filter_dataframe_gap(dframe, building, floor, department, week, day, time)
    
    trace_desks_occ = go.Bar(
        x=filtered_data_distribution['Time Slot'],
        y=filtered_data_distribution['Occupancy x Hour'],
        name='Occupancy',
        marker_color = '#6489fa'
        )

    trace_desks_ut = go.Bar(
        x=filtered_data_distribution['Time Slot'],
        y=filtered_data_distribution['Utilisation x Hour'] - filtered_data_distribution['Occupancy x Hour'],
        name='Utilisation',
        marker_color = '#fa7763'
        )

    trace_desks_number = go.Bar(
        x=filtered_data_distribution['Time Slot'],
        y=filtered_data_distribution['Number of Desks'].max() - filtered_data_distribution['Utilisation x Hour'],
        name='Number of Desks',
        marker_color = '#a9a9a9'
        )
     
    return {
        'data': [trace_desks_occ, trace_desks_ut, trace_desks_number],
        'layout': go.Layout(barmode= 'stack',
                            title='Occupancy/Utilisation Gap',
                            xaxis=dict(title='Time'),
                            yaxis=dict(title='Number of People'),
                            template="simple_white",
                            bargap=0.03)
    }

#_________________________________________________________________________________________________________________________________________________________________
#AVG&MAX OCCUPANCY BY TEAM&FLOOR (table) 

def filter_table1(dframe, building, floor, department, week, day, time):

    filtered_df = dframe.copy()
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  # Convert to list if a single building is selected
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
           
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  # Convert to list if a single floor is selected
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  # Convert to list if a single department is selected
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]

    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  # Convert to list if a single week is selected
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]


    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  # Convert to list if a single time is selected
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
    filtered_df['Occupancy x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Occupied'].transform('sum')
    filtered_df['Average Occupancy'] = round(filtered_df['Occupancy x Hour'].mean())
    filtered_df['Occupancy x Floor x Team x Hour'] = filtered_df.groupby(['Week', 'Day', 'Time','Team','Floor'])['Occupied'].transform('sum')
    filtered_df['Average Occupancy x Team'] = round(filtered_df.groupby(['Team','Floor'])['Occupancy x Floor x Team x Hour'].transform('mean'))
    filtered_df['Number of Desks x Team x Floor'] = filtered_df.groupby(['Building','Week','Day','Time','Floor','Team'])['Desk'].transform('count')
    filtered_df['Occupancy 10-4 x Floor x Team x Hour'] = filtered_df.groupby(['Week', 'Day', 'Time','Team','Floor'])['Occupied 10-4'].transform('sum')
    filtered_df['Maximum Occupancy'] = round(filtered_df['Occupancy x Hour'].max())
    
    #creating columns for further calculations
    df_10_4 = filtered_df[['Building','Floor','Team','Number of Desks x Team x Floor','Occupancy 10-4 x Hour', 'Occupancy 10-4 x Floor x Team x Hour']].dropna()
    df_10_4 = df_10_4[df_10_4['Occupancy 10-4 x Hour'] != 0]
    if not df_10_4.empty:
        df_10_4['Average Occupancy 10-4'] = round(df_10_4['Occupancy 10-4 x Hour'].mean())
        df_10_4['Average Occupancy 10-4 x Team'] = round(df_10_4.groupby(['Team', 'Floor', 'Building'])['Occupancy 10-4 x Floor x Team x Hour'].transform('mean'))

    #creating database with for all floors and buildings
    df_ooc_table = filtered_df[['Building','Floor','Team','Number of Desks x Team x Floor', 'Average Occupancy x Team']].dropna()

    if not df_10_4.empty:
        df_ooc_table['Average Occupancy 10-4 x Team'] = df_10_4[['Average Occupancy 10-4 x Team']]
        df_ooc_table['Average Occupancy 10-4 %'] = np.ceil(df_ooc_table['Average Occupancy 10-4 x Team'] / df_ooc_table['Number of Desks x Team x Floor'] * 100)
    else:
        df_ooc_table['Average Occupancy 10-4 x Team'] = 0
        df_ooc_table['Average Occupancy 10-4 %'] = 0

    df_ooc_table['Maximum Occupancy'] = filtered_df.groupby(['Building','Team','Floor'])['Occupancy x Floor x Team x Hour'].transform('max')
    df_ooc_table = df_ooc_table.drop_duplicates()
    df_ooc_table = df_ooc_table.sort_values(['Building','Floor','Team'], axis = 0, ascending = True)
    df_ooc_table['Average Occupancy %'] = np.ceil(df_ooc_table['Average Occupancy x Team']/df_ooc_table['Number of Desks x Team x Floor']*100)
    df_ooc_table['Maximum Occupancy %'] = np.ceil(df_ooc_table['Maximum Occupancy']/df_ooc_table['Number of Desks x Team x Floor']*100)
    df_ooc_table = df_ooc_table.dropna()
    df_ooc_table = df_ooc_table.drop_duplicates()


    #database for overall numbers of both building
    df_all_all=pd.DataFrame({'Building':['All'], 'Floor':['All'], 'Team':['All'], 
                     'Number of Desks x Team x Floor':[df_ooc_table['Number of Desks x Team x Floor'].sum()],
                     'Average Occupancy x Team':[df_ooc_table['Average Occupancy x Team'].sum()],
                     'Average Occupancy %':[round(df_ooc_table['Average Occupancy x Team'].sum()/df_ooc_table['Number of Desks x Team x Floor'].sum()*100)],
                     'Average Occupancy 10-4 x Team':[df_ooc_table['Average Occupancy 10-4 x Team'].sum()],
                     'Average Occupancy 10-4 %':[round(df_ooc_table['Average Occupancy 10-4 x Team'].sum()/df_ooc_table['Number of Desks x Team x Floor'].sum()*100)],
                     'Maximum Occupancy':[df_ooc_table['Maximum Occupancy'].sum()],
                     'Maximum Occupancy %':[round(df_ooc_table['Maximum Occupancy'].sum()/df_ooc_table['Number of Desks x Team x Floor'].sum()*100)],
                    })
    
    df_ooc_table_building = {}
    df_occ_building = {}
    floors__desks_building = {}
    df_ooc_table_floor = {}
    df_ooc_table_floor_final = {}
    df_occ_building_list = []
    df_occ_floor_list = []
    df_occ_floor_final = {}
    df_occ__building_final = {}
    df_occ_floor_final_list = []
    df_occ_floor_final = {}
    df_ooc_table_floor_team = {}
    df_ooc_table_floor_team_final = {}

    building_names = filtered_df['Building'].dropna().unique()
    building_names = building_names.tolist()

    #database for overall numbers of all buildings and  all floors
    for building in building_names:
        df_ooc_table_building[building] = df_ooc_table[(df_ooc_table['Building'] == building)]
        total_desks = df_ooc_table_building[building]['Number of Desks x Team x Floor'].sum()
        total_occupancy = df_ooc_table_building[building]['Average Occupancy x Team'].sum()

        # Check if total_desks is zero before calculating percentage
        if total_desks != 0:
            average_occupancy_percentage = round((total_occupancy / total_desks) * 100)
        else:
            average_occupancy_percentage = 0

        df_occ_building[building] = pd.DataFrame({'Building': [building], 'Floor': ['All'], 'Team': ['All'], 
                                                   'Number of Desks x Team x Floor': [total_desks],
                                                   'Average Occupancy x Team': [total_occupancy],
                                                   'Average Occupancy %': [average_occupancy_percentage],
                     'Average Occupancy 10-4 x Team':[df_ooc_table_building[building]['Average Occupancy 10-4 x Team'].sum()],
                     'Average Occupancy 10-4 %':[round(df_ooc_table_building[building]['Average Occupancy 10-4 x Team'].sum()/df_ooc_table_building[building]['Number of Desks x Team x Floor'].sum()*100)],
                     'Maximum Occupancy':[df_ooc_table_building[building]['Maximum Occupancy'].sum()],
                     'Maximum Occupancy %':[round(df_ooc_table_building[building]['Maximum Occupancy'].sum()/df_ooc_table_building[building]['Number of Desks x Team x Floor'].sum()*100)],
                    })

        floors__desks_building[building] = filtered_df[['Building','Floor']].dropna()
        floors__desks_building[building] = floors__desks_building[building][(floors__desks_building[building]['Building'] == building)]
        floors__desks_building[building]['Floor2'] = floors__desks_building[building]['Floor'].str.extract('(\d+)').astype(int)
        floors__desks_building[building] = floors__desks_building[building].sort_values(by = ['Floor2'])
        floors__desks_building[building] = floors__desks_building[building]['Floor'].unique().tolist()

        df_occ_floor_list = []
        for floor in floors__desks_building[building]:        
            df_ooc_table_floor[floor] = df_ooc_table[['Building','Floor','Team','Number of Desks x Team x Floor', 'Average Occupancy x Team',
                                                     'Average Occupancy %', 'Average Occupancy 10-4 x Team', 'Average Occupancy 10-4 %', 'Maximum Occupancy','Maximum Occupancy %']]
            df_ooc_table_floor[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Building'] == building]
            df_ooc_table_floor[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Floor'] == floor]

            df_ooc_table_floor_final[floor] = pd.DataFrame({'Building':[building], 'Floor':[floor], 'Team':['All'], 
                     'Number of Desks x Team x Floor':[df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()],
                     'Average Occupancy x Team':[df_ooc_table_floor[floor]['Average Occupancy x Team'].sum()],
                     'Average Occupancy %':[round(df_ooc_table_floor[floor]['Average Occupancy x Team'].sum()/df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()*100)],
                     'Average Occupancy 10-4 x Team':[df_ooc_table_floor[floor]['Average Occupancy 10-4 x Team'].sum()],
                     'Average Occupancy 10-4 %':[round(df_ooc_table_floor[floor]['Average Occupancy 10-4 x Team'].sum()/df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()*100)],
                     'Maximum Occupancy':[df_ooc_table_floor[floor]['Maximum Occupancy'].sum()],
                     'Maximum Occupancy %':[round(df_ooc_table_floor[floor]['Maximum Occupancy'].sum()/df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()*100)],
                    })

            df_ooc_table_floor_team[floor] = df_ooc_table[['Building','Floor','Team','Number of Desks x Team x Floor', 'Average Occupancy x Team',
                                                     'Average Occupancy %', 'Average Occupancy 10-4 x Team', 'Average Occupancy 10-4 %', 'Maximum Occupancy','Maximum Occupancy %']]
            df_ooc_table_floor_team[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Building'] == building]
            df_ooc_table_floor_team[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Floor'] == floor]
            df_ooc_table_floor_team_final[floor] = pd.concat([df_ooc_table_floor_final[floor],df_ooc_table_floor_team[floor]], axis = 0)        

            df_occ_floor_list.append(df_ooc_table_floor_team_final[floor])
            df_occ_floor_final = pd.concat(df_occ_floor_list)

        df_occ__building_final[building] = pd.concat([df_occ_building[building],df_occ_floor_final], axis = 0)

        df_occ_floor_final_list.append(df_occ__building_final[building])
        df_occ_floor_final = pd.concat(df_occ_floor_final_list)




    df_occ_all_final_mask = {}
    df_occ_all_final_mask_list = []

    #masking the repeated floor and building names
    for building in building_names:
        df_occ_all_final_mask[building] = df_occ_floor_final.loc[df_occ_floor_final['Building'] == building].copy()
        df_occ_all_final_mask[building]['Floor2'] = df_occ_all_final_mask[building]['Floor'].str.extract('(\d+)')
        df_occ_all_final_mask[building]['Floor2'] = df_occ_all_final_mask[building]['Floor2'].fillna(0)
        df_occ_all_final_mask[building]['Floor2'] = df_occ_all_final_mask[building]['Floor2'].astype(int)
        df_occ_all_final_mask[building] = df_occ_all_final_mask[building].sort_values(by = ['Floor2','Team'])

        df_occ_all_final_mask[building]['Building']=df_occ_all_final_mask[building]['Building'].mask(df_occ_all_final_mask[building]['Building'].duplicated(),"")
        df_occ_all_final_mask[building]['Floor']=df_occ_all_final_mask[building]['Floor'].mask(df_occ_all_final_mask[building]['Floor'].duplicated(),"")
        df_occ_all_final_mask[building] = df_occ_all_final_mask[building].fillna(0)

        df_occ_all_final_mask_list.append(df_occ_all_final_mask[building])

        df_occ_all_final_table = pd.concat(df_occ_all_final_mask_list)

    df_occ_all_final = pd.concat([df_all_all,df_occ_all_final_table], axis = 0)




    #setting columns as integers
    dict_columns_type = {'Number of Desks x Team x Floor': int,
                    'Average Occupancy x Team': int,
                         'Average Occupancy %': int,
                         'Average Occupancy 10-4 x Team': int,
                         'Average Occupancy 10-4 %': int,
                         'Maximum Occupancy': int,
                         'Maximum Occupancy %': int
                   }

    df_occ_all_final = df_occ_all_final.astype(dict_columns_type)




    #reseting indexes
    df_occ_all_final.reset_index (drop= True, inplace= True)

    #renaming the columns
    df_occ_all_final.columns = ['Building','Floor','Team','Number of Desks','Avg Occu (#)','Avg Occu (%)', 'Avg Occu 10-4 (#)', 'Avg Occu 10-4 (%)', 'Max Occu (#)', 'Max Occu (%)','Floor2']


    #setting columns with % as string and adding percentage symbol
    dict_columns_type = {'Avg Occu (%)': str,
                    'Avg Occu 10-4 (%)': str,
                         'Max Occu (%)': str,
                   }

    df_occ_all_final = df_occ_all_final.astype(dict_columns_type)

    df_occ_all_final['Avg Occu (%)'] = df_occ_all_final['Avg Occu (%)'] + '%'
    df_occ_all_final['Avg Occu 10-4 (%)'] = df_occ_all_final['Avg Occu 10-4 (%)'] + '%'
    df_occ_all_final['Max Occu (%)'] = df_occ_all_final['Max Occu (%)'] + '%'


    #making bold rows with 'all'
    indices = df_occ_all_final.index[(df_occ_all_final[["Team"]] == "All").all(1)]

    for i in indices:
        for j in range(len(df_occ_all_final.columns)):
            df_occ_all_final.iloc[i,j] = "<b>{}</b>".format(df_occ_all_final.iloc[i,j])


    return df_occ_all_final


@app.callback(
    Output('graph-table1', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_table1(building, floor, department, week, day, time):
    filtered_data_distribution = filter_table1(dframe, building, floor, department, week, day, time)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'
    
    fig_occ_fl_team = go.Table(
        columnwidth = [60,60,250,60,60,60,60,60,60,60],
      header=dict(
        values=list(['<b>Building<b>', '<b>Floor<b>', '<b>Team<b>', '<b>Number of Desks<b>', '<b>Avg Occu (#)<b>',
           '<b>Avg Occu (%)<b>', '<b>Avg Occu 10-4 (#)<b>', '<b>Avg Occu 10-4 (%)<b>',
           '<b>Max Occu (#)<b>', '<b>Max Occu (%)<b>']),
        #line_color='black',
        fill_color=headerColor,
        align=['left','left','left','left','left','left','left','left','left','left'],
        font=dict(color='black', size=9)
      ),
      cells=dict(
        values=[filtered_data_distribution['Building'], 
                filtered_data_distribution['Floor'], 
                filtered_data_distribution['Team'], 
                filtered_data_distribution['Number of Desks'], 
                filtered_data_distribution['Avg Occu (#)'], 
                filtered_data_distribution['Avg Occu (%)'], 
                filtered_data_distribution['Avg Occu 10-4 (#)'], 
                filtered_data_distribution['Avg Occu 10-4 (%)'], 
                filtered_data_distribution['Max Occu (#)'], 
                filtered_data_distribution['Max Occu (%)'], 
               ],
        #line_color='black',
        fill_color = [[rowOddColor,rowEvenColor]*56],
        align = ['left','left','left','left','left','left','left','left','left','left'],
        font = dict(color = 'black', size = 7)
        ))        
        
        
    layout = go.Layout(title="Avg & Max Occupancy by Team & Floor", title_x=0.1)
                       
    return {
        'data': [fig_occ_fl_team],
        'layout': layout
    }



#_________________________________________________________________________________________________________________________________________________________________
#AVG&MAX UTILISATION BY TEAM&FLOOR (table) 

def filter_table2(dframe, building, floor, department, week, day, time):

    filtered_df = dframe.copy()
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  # Convert to list if a single building is selected
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
           
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  # Convert to list if a single floor is selected
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  # Convert to list if a single department is selected
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]

    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  # Convert to list if a single week is selected
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]


    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  # Convert to list if a single time is selected
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
    filtered_df['Utilisation x Hour'] = filtered_df.groupby(['Week','Day','Time'])['Utilised'].transform('sum')
    filtered_df['Average Utilisation'] = round(filtered_df['Utilisation x Hour'].mean())
    filtered_df['Utilisation x Floor x Team x Hour'] = filtered_df.groupby(['Week', 'Day', 'Time','Team','Floor'])['Utilised'].transform('sum')
    filtered_df['Average Utilisation x Team'] = round(filtered_df.groupby(['Team','Floor'])['Utilisation x Floor x Team x Hour'].transform('mean'))
    filtered_df['Number of Desks x Team x Floor'] = filtered_df.groupby(['Building','Week','Day','Time','Floor','Team'])['Desk'].transform('count')
    filtered_df['Utilisation 10-4 x Floor x Team x Hour'] = filtered_df.groupby(['Week', 'Day', 'Time','Team','Floor'])['Utilised 10-4'].transform('sum')
    filtered_df['Maximum Utilisation'] = round(filtered_df['Utilisation x Hour'].max())
    
    #creating columns for further calculations
    df_10_4 = filtered_df[['Building','Floor','Team','Number of Desks x Team x Floor','Utilisation 10-4 x Hour', 'Utilisation 10-4 x Floor x Team x Hour']].dropna()
    df_10_4 = df_10_4[df_10_4['Utilisation 10-4 x Hour'] != 0]
    if not df_10_4.empty:
        df_10_4['Average Utilisation 10-4'] = round(df_10_4['Utilisation 10-4 x Hour'].mean())
        df_10_4['Average Utilisation 10-4 x Team'] = round(df_10_4.groupby(['Team', 'Floor', 'Building'])['Utilisation 10-4 x Floor x Team x Hour'].transform('mean'))

    #creating database with for all floors and buildings
    df_ooc_table = filtered_df[['Building','Floor','Team','Number of Desks x Team x Floor', 'Average Utilisation x Team']].dropna()

    if not df_10_4.empty:
        df_ooc_table['Average Utilisation 10-4 x Team'] = df_10_4[['Average Utilisation 10-4 x Team']]
        df_ooc_table['Average Utilisation 10-4 %'] = np.ceil(df_ooc_table['Average Utilisation 10-4 x Team'] / df_ooc_table['Number of Desks x Team x Floor'] * 100)
    else:
        df_ooc_table['Average Utilisation 10-4 x Team'] = 0
        df_ooc_table['Average Utilisation 10-4 %'] = 0

    df_ooc_table['Maximum Utilisation'] = filtered_df.groupby(['Building','Team','Floor'])['Utilisation x Floor x Team x Hour'].transform('max')
    df_ooc_table = df_ooc_table.drop_duplicates()
    df_ooc_table = df_ooc_table.sort_values(['Building','Floor','Team'], axis = 0, ascending = True)
    df_ooc_table['Average Utilisation %'] = np.ceil(df_ooc_table['Average Utilisation x Team']/df_ooc_table['Number of Desks x Team x Floor']*100)
    df_ooc_table['Maximum Utilisation %'] = np.ceil(df_ooc_table['Maximum Utilisation']/df_ooc_table['Number of Desks x Team x Floor']*100)
    df_ooc_table = df_ooc_table.dropna()
    df_ooc_table = df_ooc_table.drop_duplicates()


    #database for overall numbers of both building
    df_all_all=pd.DataFrame({'Building':['All'], 'Floor':['All'], 'Team':['All'], 
                     'Number of Desks x Team x Floor':[df_ooc_table['Number of Desks x Team x Floor'].sum()],
                     'Average Utilisation x Team':[df_ooc_table['Average Utilisation x Team'].sum()],
                     'Average Utilisation %':[round(df_ooc_table['Average Utilisation x Team'].sum()/df_ooc_table['Number of Desks x Team x Floor'].sum()*100)],
                     'Average Utilisation 10-4 x Team':[df_ooc_table['Average Utilisation 10-4 x Team'].sum()],
                     'Average Utilisation 10-4 %':[round(df_ooc_table['Average Utilisation 10-4 x Team'].sum()/df_ooc_table['Number of Desks x Team x Floor'].sum()*100)],
                     'Maximum Utilisation':[df_ooc_table['Maximum Utilisation'].sum()],
                     'Maximum Utilisation %':[round(df_ooc_table['Maximum Utilisation'].sum()/df_ooc_table['Number of Desks x Team x Floor'].sum()*100)],
                    })
    
    df_ooc_table_building = {}
    df_occ_building = {}
    floors__desks_building = {}
    df_ooc_table_floor = {}
    df_ooc_table_floor_final = {}
    df_occ_building_list = []
    df_occ_floor_list = []
    df_occ_floor_final = {}
    df_occ__building_final = {}
    df_occ_floor_final_list = []
    df_occ_floor_final = {}
    df_ooc_table_floor_team = {}
    df_ooc_table_floor_team_final = {}

    building_names = filtered_df['Building'].dropna().unique()
    building_names = building_names.tolist()

    #database for overall numbers of all buildings and  all floors
    for building in building_names:
        df_ooc_table_building[building] = df_ooc_table[(df_ooc_table['Building'] == building)]
        total_desks = df_ooc_table_building[building]['Number of Desks x Team x Floor'].sum()
        total_occupancy = df_ooc_table_building[building]['Average Utilisation x Team'].sum()

        # Check if total_desks is zero before calculating percentage
        if total_desks != 0:
            average_occupancy_percentage = round((total_occupancy / total_desks) * 100)
        else:
            average_occupancy_percentage = 0

        df_occ_building[building] = pd.DataFrame({'Building': [building], 'Floor': ['All'], 'Team': ['All'], 
                                                   'Number of Desks x Team x Floor': [total_desks],
                                                   'Average Utilisation x Team': [total_occupancy],
                                                   'Average Utilisation %': [average_occupancy_percentage],
                     'Average Utilisation 10-4 x Team':[df_ooc_table_building[building]['Average Utilisation 10-4 x Team'].sum()],
                     'Average Utilisation 10-4 %':[round(df_ooc_table_building[building]['Average Utilisation 10-4 x Team'].sum()/df_ooc_table_building[building]['Number of Desks x Team x Floor'].sum()*100)],
                     'Maximum Utilisation':[df_ooc_table_building[building]['Maximum Utilisation'].sum()],
                     'Maximum Utilisation %':[round(df_ooc_table_building[building]['Maximum Utilisation'].sum()/df_ooc_table_building[building]['Number of Desks x Team x Floor'].sum()*100)],
                    })

        floors__desks_building[building] = filtered_df[['Building','Floor']].dropna()
        floors__desks_building[building] = floors__desks_building[building][(floors__desks_building[building]['Building'] == building)]
        floors__desks_building[building]['Floor2'] = floors__desks_building[building]['Floor'].str.extract('(\d+)').astype(int)
        floors__desks_building[building] = floors__desks_building[building].sort_values(by = ['Floor2'])
        floors__desks_building[building] = floors__desks_building[building]['Floor'].unique().tolist()

        df_occ_floor_list = []
        for floor in floors__desks_building[building]:        
            df_ooc_table_floor[floor] = df_ooc_table[['Building','Floor','Team','Number of Desks x Team x Floor', 'Average Utilisation x Team',
                                                     'Average Utilisation %', 'Average Utilisation 10-4 x Team', 'Average Utilisation 10-4 %', 'Maximum Utilisation','Maximum Utilisation %']]
            df_ooc_table_floor[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Building'] == building]
            df_ooc_table_floor[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Floor'] == floor]

            df_ooc_table_floor_final[floor] = pd.DataFrame({'Building':[building], 'Floor':[floor], 'Team':['All'], 
                     'Number of Desks x Team x Floor':[df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()],
                     'Average Utilisation x Team':[df_ooc_table_floor[floor]['Average Utilisation x Team'].sum()],
                     'Average Utilisation %':[round(df_ooc_table_floor[floor]['Average Utilisation x Team'].sum()/df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()*100)],
                     'Average Utilisation 10-4 x Team':[df_ooc_table_floor[floor]['Average Utilisation 10-4 x Team'].sum()],
                     'Average Utilisation 10-4 %':[round(df_ooc_table_floor[floor]['Average Utilisation 10-4 x Team'].sum()/df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()*100)],
                     'Maximum Utilisation':[df_ooc_table_floor[floor]['Maximum Utilisation'].sum()],
                     'Maximum Utilisation %':[round(df_ooc_table_floor[floor]['Maximum Utilisation'].sum()/df_ooc_table_floor[floor]['Number of Desks x Team x Floor'].sum()*100)],
                    })

            df_ooc_table_floor_team[floor] = df_ooc_table[['Building','Floor','Team','Number of Desks x Team x Floor', 'Average Utilisation x Team',
                                                     'Average Utilisation %', 'Average Utilisation 10-4 x Team', 'Average Utilisation 10-4 %', 'Maximum Utilisation','Maximum Utilisation %']]
            df_ooc_table_floor_team[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Building'] == building]
            df_ooc_table_floor_team[floor] = df_ooc_table_floor[floor][df_ooc_table_floor[floor]['Floor'] == floor]
            df_ooc_table_floor_team_final[floor] = pd.concat([df_ooc_table_floor_final[floor],df_ooc_table_floor_team[floor]], axis = 0)        

            df_occ_floor_list.append(df_ooc_table_floor_team_final[floor])
            df_occ_floor_final = pd.concat(df_occ_floor_list)

        df_occ__building_final[building] = pd.concat([df_occ_building[building],df_occ_floor_final], axis = 0)

        df_occ_floor_final_list.append(df_occ__building_final[building])
        df_occ_floor_final = pd.concat(df_occ_floor_final_list)




    df_occ_all_final_mask = {}
    df_occ_all_final_mask_list = []

    #masking the repeated floor and building names
    for building in building_names:
        df_occ_all_final_mask[building] = df_occ_floor_final.loc[df_occ_floor_final['Building'] == building].copy()
        df_occ_all_final_mask[building]['Floor2'] = df_occ_all_final_mask[building]['Floor'].str.extract('(\d+)')
        df_occ_all_final_mask[building]['Floor2'] = df_occ_all_final_mask[building]['Floor2'].fillna(0)
        df_occ_all_final_mask[building]['Floor2'] = df_occ_all_final_mask[building]['Floor2'].astype(int)
        df_occ_all_final_mask[building] = df_occ_all_final_mask[building].sort_values(by = ['Floor2','Team'])

        df_occ_all_final_mask[building]['Building']=df_occ_all_final_mask[building]['Building'].mask(df_occ_all_final_mask[building]['Building'].duplicated(),"")
        df_occ_all_final_mask[building]['Floor']=df_occ_all_final_mask[building]['Floor'].mask(df_occ_all_final_mask[building]['Floor'].duplicated(),"")
        df_occ_all_final_mask[building] = df_occ_all_final_mask[building].fillna(0)

        df_occ_all_final_mask_list.append(df_occ_all_final_mask[building])

        df_occ_all_final_table = pd.concat(df_occ_all_final_mask_list)

    df_occ_all_final = pd.concat([df_all_all,df_occ_all_final_table], axis = 0)




    #setting columns as integers
    dict_columns_type = {'Number of Desks x Team x Floor': int,
                    'Average Utilisation x Team': int,
                         'Average Utilisation %': int,
                         'Average Utilisation 10-4 x Team': int,
                         'Average Utilisation 10-4 %': int,
                         'Maximum Utilisation': int,
                         'Maximum Utilisation %': int
                   }

    df_occ_all_final = df_occ_all_final.astype(dict_columns_type)




    #reseting indexes
    df_occ_all_final.reset_index (drop= True, inplace= True)

    #renaming the columns
    df_occ_all_final.columns = ['Building','Floor','Team','Number of Desks','Avg Util (#)','Avg Util (%)', 'Avg Util 10-4 (#)', 'Avg Util 10-4 (%)', 'Max Util (#)', 'Max Util (%)','Floor2']


    #setting columns with % as string and adding percentage symbol
    dict_columns_type = {'Avg Util (%)': str,
                'Avg Util 10-4 (%)': str,
                     'Max Util (%)': str,
               }

    df_occ_all_final = df_occ_all_final.astype(dict_columns_type)

    df_occ_all_final['Avg Util (%)'] = df_occ_all_final['Avg Util (%)'] + '%'
    df_occ_all_final['Avg Util 10-4 (%)'] = df_occ_all_final['Avg Util 10-4 (%)'] + '%'
    df_occ_all_final['Max Util (%)'] = df_occ_all_final['Max Util (%)'] + '%'


    #making bold rows with 'all'
    indices = df_occ_all_final.index[(df_occ_all_final[["Team"]] == "All").all(1)]

    for i in indices:
        for j in range(len(df_occ_all_final.columns)):
            df_occ_all_final.iloc[i,j] = "<b>{}</b>".format(df_occ_all_final.iloc[i,j])


    df_ut_all_final = df_occ_all_final.copy()
            
    return df_ut_all_final


@app.callback(
    Output('graph-table2', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_table2(building, floor, department, week, day, time):
    filtered_data_distribution = filter_table2(dframe, building, floor, department, week, day, time)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'
    
    fig_occ_fl_team = go.Table(
        columnwidth = [60,60,250,60,60,60,60,60,60,60],
      header=dict(
        values=list(['<b>Building<b>', '<b>Floor<b>', '<b>Team<b>', '<b>Number of Desks<b>', '<b>Avg Util (#)<b>',
       '<b>Avg Util (%)<b>', '<b>Avg Util 10-4 (#)<b>', '<b>Avg Util 10-4 (%)<b>',
       '<b>Max Util (#)<b>', '<b>Max Util (%)<b>']),
        #line_color='black',
        fill_color=headerColor,
        align=['left','left','left','left','left','left','left','left','left','left'],
        font=dict(color='black', size=9)
      ),
      cells=dict(
        values=[filtered_data_distribution['Building'], 
                filtered_data_distribution['Floor'], 
                filtered_data_distribution['Team'], 
                filtered_data_distribution['Number of Desks'], 
                filtered_data_distribution['Avg Util (#)'], 
                filtered_data_distribution['Avg Util (%)'], 
                filtered_data_distribution['Avg Util 10-4 (#)'], 
                filtered_data_distribution['Avg Util 10-4 (%)'], 
                filtered_data_distribution['Max Util (#)'], 
                filtered_data_distribution['Max Util (%)'], 
               ],
        #line_color='black',
        fill_color = [[rowOddColor,rowEvenColor]*56],
        align = ['left','left','left','left','left','left','left','left','left','left'],
        font = dict(color = 'black', size = 7)
        ))       
    
    layout = go.Layout(title="Avg & Max Utilisation by Team & Floor", title_x=0.1)
        
    return {
        'data': [fig_occ_fl_team],
        'layout': layout
    }


#_________________________________________________________________________________________________________________________________________________________________
#BANDED DESK OCCUPANCY - BY FLOOR AND TEAM


def filter_dataframe_banded_desk_occ(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time] 
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        

    df_banded_ooc_table = filtered_df[['Building','Floor','Team','Desk ref no.','Occupied']].dropna()
    df_banded_ooc_table['Percentage Desk Occupancy'] = round(((df_banded_ooc_table.groupby(['Desk ref no.'])['Occupied'].transform('sum'))/90),2)
    df_banded_ooc_table = df_banded_ooc_table.drop_duplicates(subset=['Building','Floor','Team','Desk ref no.'])

    #creating bins
    bins = [-1, 0.2, 0.4, 0.6, 0.8, 1] 
    group_names= list(['<=1 Day', '1-2 Days', '2-3 Days', '3-4 Days', '4-5 Days'])
    df_banded_ooc_table["Days Bin"] = pd.cut(df_banded_ooc_table['Percentage Desk Occupancy'], bins, labels=group_names)

    #counting number of desks
    df_banded_ooc_table['Number of Desks'] = df_banded_ooc_table.groupby(['Building','Floor','Team','Days Bin'])['Days Bin'].transform('count')
    df_banded_ooc_table = df_banded_ooc_table.copy()

    #creating final dataframe
    df_banded_ooc_table = df_banded_ooc_table[['Building','Floor','Team','Days Bin','Number of Desks']].drop_duplicates().dropna()

    #pivotting the dataframe
    df_banded_ooc_table_pivot = df_banded_ooc_table.pivot(index=['Building','Floor','Team'], columns='Days Bin', values='Number of Desks').reset_index()
    df_banded_ooc_table_pivot.columns.name=None
    df_banded_ooc_table_pivot = df_banded_ooc_table_pivot.fillna(0)

    #setting columns as integers
    pivoted_columns_type = {'<=1 Day': int,
                    '1-2 Days': int,
                         '2-3 Days': int,
                         '3-4 Days': int,
                         '4-5 Days': int
                   }

    columns_to_check = ['<=1 Day', '1-2 Days', '2-3 Days', '3-4 Days', '4-5 Days']

    for column_name in columns_to_check:
        if column_name not in df_banded_ooc_table_pivot.columns:
            df_banded_ooc_table_pivot[column_name] = 0

    df_banded_ooc_table_pivot = df_banded_ooc_table_pivot.astype(pivoted_columns_type)


    #counting totals
    df_banded_ooc_table_pivot['Total'] = (df_banded_ooc_table_pivot['<=1 Day']+df_banded_ooc_table_pivot['1-2 Days']+df_banded_ooc_table_pivot['2-3 Days']+df_banded_ooc_table_pivot['3-4 Days']+df_banded_ooc_table_pivot['4-5 Days'])


    #creating a list with names of all buildings 
    building_names = dframe['Building'].dropna().unique()
    building_names = building_names.tolist()


    df_banded_ooc_table_pivot_b = {}
    df_banded_ooc_table_pivot_b_list = []

    #for every building sorting values by floor
    for building in building_names:
        df_banded_ooc_table_pivot_b[building] = df_banded_ooc_table_pivot.loc[df_banded_ooc_table_pivot['Building'] == building].copy()

        df_banded_ooc_table_pivot_b[building]['Building']=df_banded_ooc_table_pivot_b[building]['Building'].mask(df_banded_ooc_table_pivot_b[building]['Building'].duplicated(),"")
        df_banded_ooc_table_pivot_b[building]['Floor']=df_banded_ooc_table_pivot_b[building]['Floor'].mask(df_banded_ooc_table_pivot_b[building]['Floor'].duplicated(),"")

        df_banded_ooc_table_pivot_b_list.append(df_banded_ooc_table_pivot_b[building])

        df_banded_ooc_table_pivot_final = pd.concat(df_banded_ooc_table_pivot_b_list)



    df_banded_ooc_table_total=pd.DataFrame({'Building':['Grand Total '], 'Floor':['Grand Total'], 'Team':['Grand Total'], 
                     '<=1 Day':[df_banded_ooc_table_pivot_final['<=1 Day'].sum()],
                     '1-2 Days':[df_banded_ooc_table_pivot_final['1-2 Days'].sum()],
                     '2-3 Days':[df_banded_ooc_table_pivot_final['2-3 Days'].sum()],
                     '3-4 Days':[df_banded_ooc_table_pivot_final['3-4 Days'].sum()],
                     '4-5 Days':[df_banded_ooc_table_pivot_final['4-5 Days'].sum()],
                     'Total':[df_banded_ooc_table_pivot_final['Total'].sum()]
                        })

    df_banded_ooc_table_pivot_final = pd.concat([df_banded_ooc_table_pivot_final,df_banded_ooc_table_total]).reset_index(drop = True)



    #counting grand total and making it bold
    indices = df_banded_ooc_table_pivot_final.index[(df_banded_ooc_table_pivot_final[["Floor"]] == "Grand Total").all(1)]

    for i in indices:
        for j in range(len(df_banded_ooc_table_pivot_final.columns)):
            df_banded_ooc_table_pivot_final.iloc[i,j] = "<b>{}</b>".format(df_banded_ooc_table_pivot_final.iloc[i,j])

    return df_banded_ooc_table_pivot_final


@app.callback(
    Output('table-banded-desk-occ', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_banded_desk_occ(building, floor, department, week, day, time):
    filtered_banded_desk_occ = filter_dataframe_banded_desk_occ(dframe, building, floor, department, week, day, time)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'

    fig_desk_occ = go.Table(
         columnwidth = [120,120,400,80,80,80,80,80,80],
        header=dict(values=list(['<b>Building<b>', '<b>Floor<b>', '<b>Team<b>', '<b><=1 Day<b>', '<b>1-2 Days<b>',
           '<b>2-3 Days<b>', '<b>3-4 Days<b>', '<b>4-5 Days<b>',
           '<b>Total<b>']),
                    #line_width = 0.1,
                    fill_color=headerColor,
                    align=['left','left','left','right','right','right','right','right','right'],
                    font=dict(color='black', size=9)
                   ),
        cells=dict(values=[filtered_banded_desk_occ['Building'],
                           filtered_banded_desk_occ['Floor'],
                           filtered_banded_desk_occ['Team'],
                           filtered_banded_desk_occ['<=1 Day'],
                           filtered_banded_desk_occ['1-2 Days'],
                           filtered_banded_desk_occ['2-3 Days'],
                           filtered_banded_desk_occ['3-4 Days'],
                           filtered_banded_desk_occ['4-5 Days'],
                           filtered_banded_desk_occ['Total']
                          ],
                   #line_width = 0.1,
                fill_color = [[rowOddColor,rowEvenColor]*len(filtered_banded_desk_occ)],
                align = ['left','left','left','right','right','right','right','right','right'],
                font = dict(color = 'black', size = 9)
                  ))
    
    layout = go.Layout(title="Banded Desk Occupancy", title_x=0.1)
        
    return {
        'data': [fig_desk_occ],
        'layout': layout
    }


#_________________________________________________________________________________________________________________________________________________________________
#BANDED DESK OCCUPANCY - BY FLOOR AND TEAM


def filter_dataframe_low_desk_occ(dframe, building, floor, department, week, day, time):
    filtered_df = dframe.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time] 
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
        
    df_banded_low_ooc_table = filtered_df[['Building','Floor','Team','Desk ref no.','Occupied']].dropna()
    df_banded_low_ooc_table['Percentage Desk Occupancy'] = round(((df_banded_low_ooc_table.groupby(['Desk ref no.'])['Occupied'].transform('sum'))/90),2)
    df_banded_low_ooc_table = df_banded_low_ooc_table.drop_duplicates(subset=['Building','Floor','Team','Desk ref no.'])

    #creating bins
    bins_df_banded_low_ooc_table = [-1, 0.05, 0.1, 0.2, 1,]  
    group_names_df_banded_low_ooc_table= list(['<=0.25 Days', '0.25-0.5 Days', '0.5-1 Days', '>1 Day'])
    df_banded_low_ooc_table["Days Bin"] = pd.cut(df_banded_low_ooc_table['Percentage Desk Occupancy'], bins_df_banded_low_ooc_table, labels=group_names_df_banded_low_ooc_table)

    #counting number of desks
    df_banded_low_ooc_table['Number of Desks'] = df_banded_low_ooc_table.groupby(['Building','Floor','Team','Days Bin'])['Days Bin'].transform('count')
    df_banded_low_ooc_table = df_banded_low_ooc_table.copy()
    df_banded_low_ooc_table = df_banded_low_ooc_table[['Building','Floor','Team','Days Bin','Number of Desks']].drop_duplicates().dropna() 

    #pivoting dataframe
    df_banded_low_ooc_table_pivot = df_banded_low_ooc_table.pivot(index=['Building','Floor','Team'], columns='Days Bin', values='Number of Desks').reset_index()
    df_banded_low_ooc_table_pivot.columns.name=None
    
    columns_to_check = ['<=0.25 Days', '0.25-0.5 Days', '0.5-1 Days', '>1 Day']

    # Fill missing columns with NaN
    for column_name in columns_to_check:
        if column_name not in df_banded_low_ooc_table_pivot.columns:
            df_banded_low_ooc_table_pivot[column_name] = None
            
    df_banded_low_ooc_table_pivot = df_banded_low_ooc_table_pivot.fillna(0)


    #setting columns as integers
    low_occ_pivoted_columns_type = {'<=0.25 Days': int,
                    '0.25-0.5 Days': int,
                         '0.5-1 Days': int,
                         '>1 Day': int
                   }

    df_banded_low_ooc_table_pivot = df_banded_low_ooc_table_pivot.astype(low_occ_pivoted_columns_type)


    df_banded_low_ooc_table_pivot['Total'] = (df_banded_low_ooc_table_pivot['<=0.25 Days']+df_banded_low_ooc_table_pivot['0.25-0.5 Days']+df_banded_low_ooc_table_pivot['0.5-1 Days']+df_banded_low_ooc_table_pivot['>1 Day'])


    df_banded_low_ooc_table_pivot_b = {}
    df_banded_low_ooc_table_pivot_list = []

    for building in building_names:
        df_banded_low_ooc_table_pivot_b[building] = df_banded_low_ooc_table_pivot.loc[df_banded_low_ooc_table_pivot['Building'] == building].copy()
        df_banded_low_ooc_table_pivot_b[building]['Building']=df_banded_low_ooc_table_pivot_b[building]['Building'].mask(df_banded_low_ooc_table_pivot_b[building]['Building'].duplicated(),"")
        df_banded_low_ooc_table_pivot_b[building]['Floor']=df_banded_low_ooc_table_pivot_b[building]['Floor'].mask(df_banded_low_ooc_table_pivot_b[building]['Floor'].duplicated(),"")

        df_banded_low_ooc_table_pivot_list.append(df_banded_low_ooc_table_pivot_b[building])
        df_low_occ_all_final_table = pd.concat(df_banded_low_ooc_table_pivot_list)


    df_banded_low_ooc_table_total=pd.DataFrame({'Building':['Grand Total '], 'Floor':['Grand Total'], 'Team':['Grand Total'], 
                     '<=0.25 Days':[df_low_occ_all_final_table['<=0.25 Days'].sum()],
                     '0.25-0.5 Days':[df_low_occ_all_final_table['0.25-0.5 Days'].sum()],
                     '0.5-1 Days':[df_low_occ_all_final_table['0.5-1 Days'].sum()],
                     '>1 Day':[df_low_occ_all_final_table['>1 Day'].sum()],
                     'Total':[df_low_occ_all_final_table['Total'].sum()]
                        })

    df_banded_low_ooc_table_pivot_final = pd.concat([df_low_occ_all_final_table,df_banded_low_ooc_table_total]).reset_index(drop = True)


    indices = df_banded_low_ooc_table_pivot_final.index[(df_banded_low_ooc_table_pivot_final[["Floor"]] == "Grand Total").all(1)]

    for i in indices:
        for j in range(len(df_banded_low_ooc_table_pivot_final.columns)):
            df_banded_low_ooc_table_pivot_final.iloc[i,j] = "<b>{}</b>".format(df_banded_low_ooc_table_pivot_final.iloc[i,j])

    return df_banded_low_ooc_table_pivot_final


@app.callback(
    Output('table-low-desk-occ', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_low_desk_occ(building, floor, department, week, day, time):
    filtered_low_desk_occ = filter_dataframe_low_desk_occ(dframe, building, floor, department, week, day, time)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'

    fig_low_occ = go.Table(
         columnwidth = [120,120,400,80,80,80,80,80,80],
        header=dict(values=list(['<b>Building<b>', '<b>Floor<b>', '<b>Team<b>', '<b><=0.25 Days<b>', '<b>0.25-0.5 Days<b>',
           '<b>0.5-1 Days<b>', '<b>>1 Day<b>',
           '<b>Total<b>']),
                   #line_color='black',
                    #line_width = 0.1,
                    fill_color=headerColor,
                    align=['left','left','left','right','right','right','right','right','right'],
                    font=dict(color='black', size=9)
                   ),
        cells=dict(values=[filtered_low_desk_occ['Building'],
                           filtered_low_desk_occ['Floor'],
                           filtered_low_desk_occ['Team'],
                           filtered_low_desk_occ['<=0.25 Days'],
                           filtered_low_desk_occ['0.25-0.5 Days'],
                           filtered_low_desk_occ['0.5-1 Days'],
                           filtered_low_desk_occ['>1 Day'],
                           filtered_low_desk_occ['Total']
                          ],
                #line_color='black',
                   #line_width = 0.1,
                fill_color = [[rowOddColor,rowEvenColor]*len(filtered_low_desk_occ)],
                align = ['left','left','left','right','right','right','right','right','right'],
                font = dict(color = 'black', size = 9)
                  ))

    layout = go.Layout(title="Low Occupancy Desks", title_x=0.1)
        
    return {
        'data': [fig_low_occ],
        'layout': layout
    }

#_________________________________________________________________________________________________________________________________________________________________
#NUMBER OF MEETING ROOMS IN USE



def filter_dataframe_number_meeting_rooms(dframe, building, floor, department, week, day, time):
    filtered_df = dframe_meeting.copy()

    filtered_df['Meeting Rooms in Use'] = filtered_df[(filtered_df['Type'] == 'Meeting Room')].groupby(['Week','Day','Time'])['Hours in Use'].transform('sum')

    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time] 
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
    df_meeting = filtered_df[['Week','Day','Time','Meeting Rooms in Use']].dropna().drop_duplicates()
    df_meeting['Week'] = df_meeting['Week'].apply(lambda x: str(int(float(x))) if str(x).replace('.', '', 1).isdigit() else None)
    df_meeting = df_meeting.dropna(subset=['Week'])
    df_meeting['Time Slot'] = df_meeting['Time'] + ', ' + df_meeting['Day'] + ', Week ' + df_meeting['Week'] 
    
    return df_meeting


@app.callback(
    Output('graph-number-meeting-rooms', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_number_meeting_rooms(building, floor, department, week, day, time):
    filtered_data_number_meeting_rooms = filter_dataframe_number_meeting_rooms(dframe, building, floor, department, week, day, time)
    
    trace = go.Bar(x=filtered_data_number_meeting_rooms["Time Slot"],
                                y=(filtered_data_number_meeting_rooms["Meeting Rooms in Use"]), 
                                marker_color='#26A2ED')
    
    avg = round((filtered_data_number_meeting_rooms["Meeting Rooms in Use"]).mean())
    
    avg_trace = go.Scatter(
        x=filtered_data_number_meeting_rooms['Time Slot'],
        y=[avg] * len(filtered_data_number_meeting_rooms['Time Slot']),
        name='Average',
        mode='lines',
        line_dash ='dot', marker_color = 'Black',
        showlegend=False
    )    
    
    layout = go.Layout(title_text="Number of Meeting Rooms in Use",
                            template="simple_white",
                            bargap=0.03,
                            showlegend=False,
                            yaxis_range = [0,dframe_meeting['Number of Meeting Rooms'].max()])
    
    return {
        'data': [trace, avg_trace],
        'layout': layout
    }

#_________________________________________________________________________________________________________________________________________________________________
#NUMBER OF BREAKOUT SPACES IN USE

def filter_dataframe_number_breakout_spaces(dframe, building, floor, department, week, day, time):
    filtered_df = dframe_meeting.copy()

    filtered_df['Breakout Spaces in Use'] = filtered_df[(filtered_df['Type'] == 'Breakout Space')].groupby(['Week','Day','Time'])['Hours in Use'].transform('sum')
    filtered_df = filtered_df[(filtered_df['Type'] == 'Breakout Space')]
    filtered_df['Week'] = filtered_df['Week'].apply(lambda x: str(int(float(x))) if str(x).replace('.', '', 1).isdigit() else None)

    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]  
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]

    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)] 
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
     
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time] 
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    df_breakout = filtered_df[['Week','Day','Time','Breakout Spaces in Use']].dropna()
    df_breakout = df_breakout.drop_duplicates()
    df_breakout['Week'] = df_breakout['Week'].astype(int)
    df_breakout['Week'] = df_breakout['Week'].astype(str)
    df_breakout['Time Slot'] = df_breakout['Time'] + ', ' + df_breakout['Day'] + ', Week ' + df_breakout['Week'] 
       
    return df_breakout


@app.callback(
    Output('graph-number-breakout-spaces', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_number_breakout_spaces(building, floor, department, week, day, time):
    filtered_data_number_breakout_spaces = filter_dataframe_number_breakout_spaces(dframe, building, floor, department, week, day, time)
    
    trace = go.Bar(x=filtered_data_number_breakout_spaces["Time Slot"],
                   y=(filtered_data_number_breakout_spaces["Breakout Spaces in Use"]),
                   showlegend=False,
                   marker_color='#26A2ED')
    
    avg = round((filtered_data_number_breakout_spaces["Breakout Spaces in Use"]).mean())
    
    avg_trace = go.Scatter(
        x=filtered_data_number_breakout_spaces['Time Slot'],
        y=[avg] * len(filtered_data_number_breakout_spaces['Time Slot']),
        name='Average',
        mode='lines',
        line_dash ='dot', marker_color = 'Black',
        showlegend=False
    )    
    
    return {
        'data': [trace, avg_trace],
        'layout': go.Layout(title_text="Number of Breakout Spaces in Use",
                            template='simple_white',
                            bargap=0.03,
                            showlegend=False,
                            yaxis_range = [0,dframe_meeting['Number of Breakout Spaces'].max()],
                            yaxis_title_text="Number of Breakout Spaces in Use",
                            xaxis_title_text="Time")
    }

#_________________________________________________________________________________________________________________________________________________________________
#NUMBER OF MEETING SPACES IN USE BY TYPE 

def filter_dataframe_spaces_type(dframe, building, floor, department, week, day, time):
    filtered_df = dframe_meeting.copy()
    filtered_df['Week'] = filtered_df['Week'].apply(lambda x: str(int(float(x))) if str(x).replace('.', '', 1).isdigit() else None)

    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building]
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
 
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
            
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
                    
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
            
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    color_palette = ['#98C7DC', '#B2A1E2', '#F99B15', '#F05050', '#F4D646', '#41C572', '#26A2ED', '#966496', '#B8860B', '#FF7F50']

    number_meeting = {}
    trace_space = {}
    traces_list = []

    type_meeting = filtered_df[['Type']].dropna()
    type_meeting = type_meeting['Type'].unique().tolist()
    type_meeting = [type_item for type_item in type_meeting if type_item != 0]

        
    for space in type_meeting:
        number_meeting[space] = filtered_df[['Week','Day','Time','Type','Number of Meeting Spaces in Use x Type']].dropna()
        number_meeting[space] = number_meeting[space][(number_meeting[space]['Type'] == space)]
        number_meeting[space] = number_meeting[space].drop_duplicates()
        number_meeting[space]['Week'] = number_meeting[space]['Week'].apply(lambda x: int(float(x)) if x.replace('.', '', 1).isdigit() else None)
        number_meeting[space]['Week'] = number_meeting[space]['Week'].astype(str)
        number_meeting[space]['Time Slot'] = number_meeting[space]['Time'] + ', ' + number_meeting[space]['Day'] + ', Week ' + number_meeting[space]['Week']

        trace_space[space] =  go.Bar(
        x=number_meeting[space]['Time Slot'],
        y=number_meeting[space]['Number of Meeting Spaces in Use x Type'],
        name=space,
        marker_color = random.choice(color_palette)
        )

        traces_list.append(trace_space[space])
    
    
    return traces_list


@app.callback(
    Output('graph-spaces-type', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_spaces_type(building, floor, department, week, day, time):
    traces_type = filter_dataframe_spaces_type(dframe, building, floor, department, week, day, time)
    
    return {
        'data': traces_type,
        'layout': go.Layout(barmode= 'stack',
                            title='Number of Meeting Spaces in Use by Type',
                            xaxis=dict(title='Time'),
                            yaxis=dict(title='Number of People'),
                            template="simple_white",
                            bargap=0.03)
    }


#_________________________________________________________________________________________________________________________________________________________________
#MEETING SIZE VS MEETING ROOM SIZE BY BUILDING

def filter_dataframe_meeting_vs_size(dframe, building, floor, department, week, day, time):
    filtered_df = dframe_meeting.copy()

    meeting_rooms = dframe_meeting['Number of Meeting Rooms'].dropna()
    unique_meeting_rooms = meeting_rooms.unique()
    sum_unique_meeting_rooms = sum(unique_meeting_rooms)
    filtered_df['Week'] = filtered_df['Week'].apply(lambda x: str(int(float(x))) if str(x).replace('.', '', 1).isdigit() else None)
        
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]
                
    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor]  
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]

    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]  
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
                
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week]  
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]

    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
     
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time]  
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]

    dframe_meeting_ppl = filtered_df[['Space ref no.','Type','#ppl']]
    dframe_meeting_ppl = dframe_meeting_ppl[(dframe_meeting_ppl['Type'] == 'Meeting Room')]

    bins= [0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 100] 
    group_names= list(['1', '2', '3-4', '5-6', '7-8', '9-10', '11-12', '13-14', '15-16', '16+'])
    dframe_meeting_ppl["Capacity Bin"] = pd.cut(dframe_meeting_ppl["#ppl"], bins, labels=group_names)
    dframe_meeting_ppl["Unique Count People Bin"] = dframe_meeting_ppl.groupby(['Capacity Bin'])['Capacity Bin'].transform('count')
    dframe_meeting_ppl = dframe_meeting_ppl.dropna()

    dframe_meeting_ppl["% of Meetings"] = dframe_meeting_ppl["Unique Count People Bin"]/ len(dframe_meeting_ppl['Space ref no.'])
    dframe_meeting_ppl = dframe_meeting_ppl.sort_values(by = 'Capacity Bin')

    dframe_meeting_ppl_val = dframe_meeting_ppl[['Capacity Bin','% of Meetings']].drop_duplicates()

    dframe_meeting_size = dframe_meeting[['Space ref no.','Type','Number of Meeting Rooms','Capacity']]
    dframe_meeting_size = dframe_meeting_size[(dframe_meeting_size['Type'] == 'Meeting Room')]
    dframe_meeting_size = dframe_meeting_size.drop_duplicates()

    dframe_meeting_size["Capacity Bin"] = pd.cut(dframe_meeting_size["Capacity"], bins, labels=group_names)
    dframe_meeting_size["Unique Count Capacity Bin"] = dframe_meeting_size.groupby(['Capacity Bin'])['Capacity Bin'].transform('count')

    dframe_meeting_size["% of Meeting Rooms"] = dframe_meeting_size["Unique Count Capacity Bin"]/ sum_unique_meeting_rooms
    dframe_meeting_size = dframe_meeting_size.sort_values(by = 'Capacity Bin')

    dframe_meeting_size_val = dframe_meeting_size[['Capacity Bin','% of Meeting Rooms']].drop_duplicates()

    dframe_meetings_final = dframe_meeting_ppl_val.merge(dframe_meeting_size_val[['Capacity Bin', '% of Meeting Rooms']], on = 'Capacity Bin', how = 'outer')
    dframe_meetings_final = dframe_meetings_final.sort_values(by = 'Capacity Bin')
       
    return dframe_meetings_final 


@app.callback(
    Output('graph-meeting-vs-size', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_meeting_vs_size(building, floor, department, week, day, time):
    filtered_data_meeting_vs_size = filter_dataframe_meeting_vs_size(dframe, building, floor, department, week, day, time)
    
    trace_meeting_ppl = go.Bar(
        x=filtered_data_meeting_vs_size['Capacity Bin'],
        y=filtered_data_meeting_vs_size['% of Meetings'],
        name='% of Meetings',
        marker_color = '#41C572'
        )

    trace_meeting_size = go.Bar(
        x=filtered_data_meeting_vs_size["Capacity Bin"],
        y=filtered_data_meeting_vs_size["% of Meeting Rooms"],
        name="% of Meeting Rooms",
        marker_color = '#26A2ED'
        )
     
    return {
        'data': [trace_meeting_ppl, trace_meeting_size],
            'layout': go.Layout(barmode= 'group',
                                title='Meeting Size vs. Meeting Room Size (Banded) ',
                                xaxis=dict(title='Size (number of people)'),
                                template="simple_white",
                                yaxis_tickformat = ".0%")
    }


#_________________________________________________________________________________________________________________________________________________________________
#MEETING SPACES POPULATION BY TIME


def filter_meeting_space_pop(dframe, building, floor, department, week, day):
    filtered_df = dframe_meeting.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]

        
    #creating new dataframe with relevant columns
    df_popul_x_time = filtered_df[['Time','Day','Week','Building','Floor','Type','#ppl']].copy()
    df_popul_x_time['#ppl'] = df_popul_x_time['#ppl'].fillna(0)

    #setting column types
    df_popul_x_time_columns_type = {'Time': str,
                    'Day': str,
                         'Week': int,
                         'Building': str,
                         'Floor': str,
                         'Type': str,
                         '#ppl': int
                   }

    df_popul_x_time = df_popul_x_time.astype(df_popul_x_time_columns_type)


    #formulas for average and maximum populations
    df_popul_x_time['Population x Hour x Building x Floor x Type'] = df_popul_x_time.groupby(['Time','Day','Week','Building','Floor','Type'])['#ppl'].transform('sum').copy()
    df_popul_x_time['Avg'] = (round(df_popul_x_time.groupby(['Time','Type','Floor','Building'])['Population x Hour x Building x Floor x Type'].transform('mean'))).astype(int)
    df_popul_x_time['Max'] = round(df_popul_x_time.groupby(['Time','Type','Floor','Building'])['Population x Hour x Building x Floor x Type'].transform('max')).astype(int)
    df_popul_x_time = df_popul_x_time.copy()


    #dataframe with final columns
    df_popul_x_time=df_popul_x_time[['Time','Building','Floor','Type','Avg','Max']].drop_duplicates()

    #pivoting dataframe
    df_popul_x_time_pivoted = df_popul_x_time.pivot(index=['Building','Floor','Type'], columns=['Time'], values=['Avg', 'Max'])                .reset_index()
    df_popul_x_time_pivoted.columns.name=None


    #swapping axises
    df_popul_x_time_pivoted_final = df_popul_x_time_pivoted.swaplevel(0,1,axis = 1).sort_index(axis = 1)


    #creating a list with names of all buildings 
    building_names = dframe_meeting['Building'].dropna().unique()
    building_names = building_names.tolist()


    df_popul_x_time_pivoted_b = {}
    df_popul_x_time_pivoted_b_list = []

    #for every building sorting values by floor
    for building in building_names:
        df_popul_x_time_pivoted_b[building] = df_popul_x_time_pivoted.loc[df_popul_x_time_pivoted[('Building',     '')] == building].copy()

        df_popul_x_time_pivoted_b[building][(  'Floor2',     '')] = df_popul_x_time_pivoted_b[building][(   'Floor',     '')].str.extract('(\d+)').astype(int)
        df_popul_x_time_pivoted_b[building] = df_popul_x_time_pivoted_b[building].sort_values(by = [(  'Floor2',     ''),(    'Type',     '')])

        df_popul_x_time_pivoted_b[building][('Building',     '')]=df_popul_x_time_pivoted_b[building][('Building',     '')].mask(df_popul_x_time_pivoted_b[building][('Building',     '')].duplicated(),"")
        df_popul_x_time_pivoted_b[building][(   'Floor',     '')]=df_popul_x_time_pivoted_b[building][(   'Floor',     '')].mask(df_popul_x_time_pivoted_b[building][(   'Floor',     '')].duplicated(),"")
        df_popul_x_time_pivoted_b[building] = df_popul_x_time_pivoted_b[building].fillna(0)

        df_popul_x_time_pivoted_b_list.append(df_popul_x_time_pivoted_b[building])

        df_popul_x_time_pivoted_final = pd.concat(df_popul_x_time_pivoted_b_list)


    #setting correct order of columns
    name_order = [('Building',     ''),
                (   'Floor',     ''),
                (    'Type',     ''),
                (     'Avg',  '9am'),
                (     'Avg', '10am'),
                (     'Avg', '11am'),
                (     'Avg', '12pm'),
                (     'Avg',  '1pm'),
                (     'Avg',  '2pm'),
                (     'Avg',  '3pm'),
                (     'Avg',  '4pm'),
                (     'Avg',  '5pm'),
                  (     'Max',  '9am'),
                (     'Max', '10am'),
                (     'Max', '11am'),
                (     'Max', '12pm'),
                (     'Max',  '1pm'),
                (     'Max',  '2pm'),
                (     'Max',  '3pm'),
                (     'Max',  '4pm'),
                (     'Max',  '5pm'),
                (  'Floor2',     '')]

    df_popul_x_time_pivoted_final = df_popul_x_time_pivoted_final[name_order]
    df_popul_x_time_pivoted_final_copy = df_popul_x_time_pivoted_final


    df_popul_x_time_pivoted_final_copy = df_popul_x_time_pivoted_final_copy.swaplevel(0,1,axis = 1).sort_index(axis = 1)


        
    return df_popul_x_time_pivoted_final_copy


@app.callback(
    Output('table-meeting-space-popul', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value')
    ]
)

def update_meeting_space_pop(building, floor, department, week, day):
    filtered_meeting_space_pop = filter_meeting_space_pop(dframe, building, floor, department, week, day)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'

    fig_df_popul_x_time_pivoted = go.Table(
         columnwidth = [80,80,80,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50],
        header=dict(values=list([(    '', '<b>Building<b>'),
                    (    '',    '<b>Floor<b>'),
                    (    '',     '<b>Type<b>'),
                    ( '<b>9am<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ('<b>10am<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ('<b>11am<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ('<b>12pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>1pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>2pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>3pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>4pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>5pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>')]),
                   #line_color='black',
                    #line_width = 0.5,
                    fill_color=headerColor,
                    align=['left','left','left','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right'],
                    font=dict(color='black', size=9)
                   ),
        cells=dict(values=[filtered_meeting_space_pop[(    '', 'Building')],
                           filtered_meeting_space_pop[(    '',    'Floor')],
                           filtered_meeting_space_pop[(    '',     'Type')],
                           filtered_meeting_space_pop[( '9am',      'Avg')],
                           filtered_meeting_space_pop[( '9am',      'Max')],
                           filtered_meeting_space_pop[('10am',      'Avg')],
                           filtered_meeting_space_pop[('10am',      'Max')],
                           filtered_meeting_space_pop[('11am',      'Avg')],
                           filtered_meeting_space_pop[('11am',      'Max')],
                           filtered_meeting_space_pop[('12pm',      'Avg')],
                           filtered_meeting_space_pop[('12pm',      'Max')],
                           filtered_meeting_space_pop[( '1pm',      'Avg')],
                           filtered_meeting_space_pop[( '1pm',      'Max')],
                           filtered_meeting_space_pop[( '2pm',      'Avg')],
                           filtered_meeting_space_pop[( '2pm',      'Max')],
                           filtered_meeting_space_pop[( '3pm',      'Avg')],
                           filtered_meeting_space_pop[( '3pm',      'Max')],
                           filtered_meeting_space_pop[( '4pm',      'Avg')],
                           filtered_meeting_space_pop[( '5pm',      'Max')],
                           filtered_meeting_space_pop[( '4pm',      'Avg')],
                           filtered_meeting_space_pop[( '5pm',      'Max')],
                          ],
                   #line_width = 0.1,
                fill_color = [[rowOddColor,rowEvenColor]*len(filtered_meeting_space_pop)],
                align=['left','left','left','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right'],
                font = dict(color = 'black', size = 9)
                  ))


    layout = go.Layout(title="Meeting Space Population by Time", title_x=0.1)
        
    return {
        'data': [fig_df_popul_x_time_pivoted],
        'layout': layout
    }


#_________________________________________________________________________________________________________________________________________________________________
#MEETING SPACES IN USE BY TIME


def filter_meeting_space_use(dframe, building, floor, department, week, day):
    filtered_df = dframe_meeting.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]

        
    df_spaces_used_x_time = filtered_df[['Time','Day','Week','Building','Floor','Type','Hours in Use']].copy()
    df_spaces_used_x_time['Number of Meeting Spaces in Use x Type'] = filtered_df.groupby (['Building','Day','Time','Week','Type'])['Hours in Use']. transform('sum')


    #setting column types
    df_spaces_used_x_time_columns_type = {'Time': str,
                    'Day': str,
                         'Building': str,
                         'Floor': str,
                         'Type': str,
                         'Number of Meeting Spaces in Use x Type': int
                   }

    df_spaces_used_x_time = df_spaces_used_x_time.astype(df_spaces_used_x_time_columns_type)


    #formulas for average and maximum populations
    df_spaces_used_x_time['Avg'] = (round(df_spaces_used_x_time.groupby(['Time','Type','Floor','Building'])['Number of Meeting Spaces in Use x Type'].transform('mean'))).astype(int)
    df_spaces_used_x_time['Max'] = round(df_spaces_used_x_time.groupby(['Time','Type','Floor','Building'])['Number of Meeting Spaces in Use x Type'].transform('max')).astype(int)
    df_spaces_used_x_time = df_spaces_used_x_time.copy()


    #dataframe with final columns
    df_spaces_used_x_time=df_spaces_used_x_time[['Time','Building','Floor','Type','Avg','Max']].drop_duplicates()


    #pivoting dataframe
    df_spaces_used_x_time_pivoted = df_spaces_used_x_time.pivot(index=['Building','Floor','Type'], columns=['Time'], values=['Avg', 'Max'])                .reset_index()
    df_spaces_used_x_time_pivoted.columns.name=None


    df_spaces_used_x_time_pivoted_final = df_spaces_used_x_time_pivoted.swaplevel(0,1,axis = 1).sort_index(axis = 1)


    #creating a list with names of all buildings 
    building_names = dframe_meeting['Building'].dropna().unique()
    building_names = building_names.tolist()


    df_spaces_used_x_time_pivoted_b = {}
    df_spaces_used_x_time_pivoted_b_list = []

    #for every building sorting values by floor
    for building in building_names:
        df_spaces_used_x_time_pivoted_b[building] = df_spaces_used_x_time_pivoted.loc[df_spaces_used_x_time_pivoted[('Building',     '')] == building].copy()

        df_spaces_used_x_time_pivoted_b[building][(  'Floor2',     '')] = df_spaces_used_x_time_pivoted_b[building][(   'Floor',     '')].str.extract('(\d+)').astype(int)
        df_spaces_used_x_time_pivoted_b[building] = df_spaces_used_x_time_pivoted_b[building].sort_values(by = [(  'Floor2',     ''),(    'Type',     '')])

        df_spaces_used_x_time_pivoted_b[building][('Building',     '')]=df_spaces_used_x_time_pivoted_b[building][('Building',     '')].mask(df_spaces_used_x_time_pivoted_b[building][('Building',     '')].duplicated(),"")
        df_spaces_used_x_time_pivoted_b[building][(   'Floor',     '')]=df_spaces_used_x_time_pivoted_b[building][(   'Floor',     '')].mask(df_spaces_used_x_time_pivoted_b[building][(   'Floor',     '')].duplicated(),"")
        df_spaces_used_x_time_pivoted_b[building] = df_spaces_used_x_time_pivoted_b[building].fillna(0)

        df_spaces_used_x_time_pivoted_b_list.append(df_spaces_used_x_time_pivoted_b[building])

        df_spaces_used_x_time_pivoted_final = pd.concat(df_spaces_used_x_time_pivoted_b_list)


    #setting correct order of columns
    name_order = [('Building',     ''),
                (   'Floor',     ''),
                (    'Type',     ''),
                (     'Avg',  '9am'),
                (     'Avg', '10am'),
                (     'Avg', '11am'),
                (     'Avg', '12pm'),
                (     'Avg',  '1pm'),
                (     'Avg',  '2pm'),
                (     'Avg',  '3pm'),
                (     'Avg',  '4pm'),
                (     'Avg',  '5pm'),
                  (     'Max',  '9am'),
                (     'Max', '10am'),
                (     'Max', '11am'),
                (     'Max', '12pm'),
                (     'Max',  '1pm'),
                (     'Max',  '2pm'),
                (     'Max',  '3pm'),
                (     'Max',  '4pm'),
                (     'Max',  '5pm'),
                (  'Floor2',     '')]

    df_spaces_used_x_time_pivoted_final = df_spaces_used_x_time_pivoted_final[name_order]
    df_spaces_used_x_time_pivoted_final_copy = df_spaces_used_x_time_pivoted_final


    df_spaces_used_x_time_pivoted_final_copy = df_spaces_used_x_time_pivoted_final_copy.swaplevel(0,1,axis = 1).sort_index(axis = 1)


    return df_spaces_used_x_time_pivoted_final_copy


@app.callback(
    Output('table-meeting-space-use', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value')
    ]
)

def update_meeting_space_use(building, floor, department, week, day):
    filtered_meeting_space_use = filter_meeting_space_use(dframe, building, floor, department, week, day)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'

    fig_df_spaces_used_x_time_pivoted = go.Table(
         columnwidth = [80,80,80,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50],
        header=dict(values=list([(    '', '<b>Building<b>'),
                    (    '',    '<b>Floor<b>'),
                    (    '',     '<b>Type<b>'),
                    ( '<b>9am<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ('<b>10am<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ('<b>11am<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ('<b>12pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>1pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>2pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>3pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>4pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>'),
                    ( '<b>5pm<b>',      '<b>Avg<b>'),
                    (    '',      '<b>Max<b>')]),
                    #line_width = 0.1,
                    fill_color=headerColor,
                    align=['left','left','left','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right'],
                    font=dict(color='black', size=9)
                   ),
        cells=dict(values=[filtered_meeting_space_use[(    '', 'Building')],
                           filtered_meeting_space_use[(    '',    'Floor')],
                           filtered_meeting_space_use[(    '',     'Type')],
                           filtered_meeting_space_use[( '9am',      'Avg')],
                           filtered_meeting_space_use[( '9am',      'Max')],
                           filtered_meeting_space_use[('10am',      'Avg')],
                           filtered_meeting_space_use[('10am',      'Max')],
                           filtered_meeting_space_use[('11am',      'Avg')],
                           filtered_meeting_space_use[('11am',      'Max')],
                           filtered_meeting_space_use[('12pm',      'Avg')],
                           filtered_meeting_space_use[('12pm',      'Max')],
                           filtered_meeting_space_use[( '1pm',      'Avg')],
                           filtered_meeting_space_use[( '1pm',      'Max')],
                           filtered_meeting_space_use[( '2pm',      'Avg')],
                           filtered_meeting_space_use[( '2pm',      'Max')],
                           filtered_meeting_space_use[( '3pm',      'Avg')],
                           filtered_meeting_space_use[( '3pm',      'Max')],
                           filtered_meeting_space_use[( '4pm',      'Avg')],
                           filtered_meeting_space_use[( '5pm',      'Max')],
                           filtered_meeting_space_use[( '4pm',      'Avg')],
                           filtered_meeting_space_use[( '5pm',      'Max')],
                          ],
                #line_color='black',
                   #line_width = 0.1,
                fill_color = [[rowOddColor,rowEvenColor]*len(filtered_meeting_space_use)],
                align=['left','left','left','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right','right'],
                font = dict(color = 'black', size = 9)
                  ))


    layout = go.Layout(title="Meeting Space in Use by Time", title_x=0.1)
        
    return {
        'data': [fig_df_spaces_used_x_time_pivoted],
        'layout': layout
    }


#_________________________________________________________________________________________________________________________________________________________________
#MEETING ROOMS AVERAGE AND MAXIMUM POPULATIONS


def filter_meeting_room_pop(dframe, building, floor, department, week, day, time):
    filtered_df = dframe_meeting.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time] 
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
    df_room_popul = filtered_df[['Building','Floor','Name','Capacity','Hours in Use','#ppl']].copy()
    df_room_popul = df_room_popul[((df_room_popul['Name'] != 'Café') & (filtered_df['Name'] != 'Kitchen Table') & (filtered_df['Name'] != 'Standing Table ') & (filtered_df['Name'] != 'Unnamed'))]
    df_room_popul['Avg Population'] = (round(df_room_popul.groupby(['Building','Floor','Name'])['#ppl'].transform('mean')))
    df_room_popul['Max Population'] = round(df_room_popul.groupby(['Building','Floor','Name'])['#ppl'].transform('max'))
    df_room_popul['Hours in Use by Room'] = (round(((df_room_popul.groupby(['Building','Name'])['Hours in Use'].transform('sum'))/90),2)*100)
    df_room_popul = df_room_popul.drop(['#ppl','Hours in Use'],axis=1)
    df_room_popul = df_room_popul.drop_duplicates()
    df_room_popul = df_room_popul.fillna(0)

    #formulas for average and maximum populations
    df_room_popul['Avg Population'] = df_room_popul['Avg Population'].astype(int)
    df_room_popul['Max Population'] = df_room_popul['Max Population'].astype(int)
    df_room_popul['Hours in Use by Room'] = df_room_popul['Hours in Use by Room'].astype(int).astype(str)
    df_room_popul['Hours in Use by Room'] = df_room_popul['Hours in Use by Room'] + '%'


    #creating a list with names of all buildings 
    building_names = dframe_meeting['Building'].dropna().unique()
    building_names = building_names.tolist()


    df_room_popul_b = {}
    df_room_popul_b_list = []

    #for every building sorting values by floor
    for building in building_names:
        df_room_popul_b[building] = df_room_popul.loc[df_room_popul['Building'] == building].copy()

        df_room_popul_b[building]['Floor2'] = df_room_popul_b[building]['Floor'].str.extract('(\d+)').astype(int)
        df_room_popul_b[building] = df_room_popul_b[building].sort_values(by = ['Floor2','Name'])

        df_room_popul_b[building]['Building']=df_room_popul_b[building]['Building'].mask(df_room_popul_b[building]['Building'].duplicated(),"")
        df_room_popul_b[building]['Floor']=df_room_popul_b[building]['Floor'].mask(df_room_popul_b[building]['Floor'].duplicated(),"")
        df_room_popul_b[building] = df_room_popul_b[building].fillna(0)

        df_room_popul_b_list.append(df_room_popul_b[building])

        df_room_popul_final = pd.concat(df_room_popul_b_list)

    return df_room_popul_final


@app.callback(
    Output('table-meeting-room-pop', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_meeting_room_pop(building, floor, department, week, day, time):
    filtered_banded_desk_occ = filter_meeting_room_pop(dframe, building, floor, department, week, day, time)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'

    fig_avg_max_popul = go.Table(
         #columnwidth = [120,120,400,80,80,80,80,80,80],
        header=dict(values=list(['<b>Building<b>', '<b>Floor<b>', '<b>Name<b>', '<b>Capacity<b>', '<b>Avg Population<b>',
           '<b>Max Population<b>', '<b>Hours in Use<b>']),
                    #line_width = 0.5,
                    fill_color=headerColor,
                    align=['left','left','right','right','right','right','right'],
                    font=dict(color='black', size=9)
                   ),
        cells=dict(values=[filtered_banded_desk_occ['Building'],
                           filtered_banded_desk_occ['Floor'],
                           filtered_banded_desk_occ['Name'],
                           filtered_banded_desk_occ['Capacity'],
                           filtered_banded_desk_occ['Avg Population'],
                           filtered_banded_desk_occ['Max Population'],
                           filtered_banded_desk_occ['Hours in Use by Room'],
                          ],
                   #line_width = 0.1,
                fill_color = [[rowOddColor,rowEvenColor]*len(filtered_banded_desk_occ)],
                align = ['left','left','right','right','right','right','right'],
                font = dict(color = 'black', size = 9)
                  ))
    
    layout = go.Layout(title="Meeting Rooms Population", title_x=0.1)
        
    return {
        'data': [fig_avg_max_popul],
        'layout': layout
    }

#_________________________________________________________________________________________________________________________________________________________________
#NUMBER OF MEETING SPACES IN USE 


def filter_meeting_spaces_in_use(dframe, building, floor, department, week, day, time):
    filtered_df = dframe_meeting.copy()
    
    # Filter by building
    if building and len(building) > 0:
        if isinstance(building, str):
            building = [building] 
        filtered_df = filtered_df[filtered_df['Building'].isin(building)]

    # Filter by floor
    if floor and len(floor) > 0:
        if isinstance(floor, str):
            floor = [floor] 
        filtered_df = filtered_df[filtered_df['Floor'].isin(floor)]
        
    # Filter by department
    if 'Team' in filtered_df.columns and department and len(department) > 0:
        if isinstance(department, str):
            department = [department]
        filtered_df = filtered_df[filtered_df['Team'].isin(department)]
        
    # Filter by week
    if week and len(week) > 0:
        if isinstance(week, str):
            week = [week] 
        filtered_df = filtered_df[filtered_df['Week 2'].isin(week)]
        
    # Filter by day
    if day and len(day) > 0:
        if isinstance(day, str):
            day = [day]  
        filtered_df = filtered_df[filtered_df['Day'].isin(day)]
        
    # Filter by time
    if time and len(time) > 0:
        if isinstance(time, str):
            time = [time] 
        filtered_df = filtered_df[filtered_df['Time'].isin(time)]
        
    df_meeting_spaces_used_floor = filtered_df[['Week','Day','Time','Building','Floor','Type','Space ref no.','Hours in Use']].copy()
    df_meeting_spaces_used_floor['Rooms Occupied'] = df_meeting_spaces_used_floor.groupby(['Week','Day','Time','Building','Floor','Type'])['Hours in Use'].transform('sum')
    df_meeting_spaces_used_floor['Number of Meeting Spaces'] = df_meeting_spaces_used_floor.groupby(['Building','Floor','Type'])['Space ref no.'].transform('nunique')
    df_meeting_spaces_used_floor['Avg Number in Use'] = round(df_meeting_spaces_used_floor.groupby(['Building','Floor','Type'])['Rooms Occupied'].transform('mean'))
    df_meeting_spaces_used_floor['Max Number in Use'] = round(df_meeting_spaces_used_floor.groupby(['Building','Floor','Type'])['Rooms Occupied'].transform('max'))

    df_meeting_spaces_used_floor = df_meeting_spaces_used_floor.drop(['Week','Day','Time','Space ref no.','Rooms Occupied'],axis=1)
    df_meeting_spaces_used_floor = df_meeting_spaces_used_floor.drop_duplicates()


    #setting types of columns
    df_meeting_spaces_used_floor_columns_type = {'Number of Meeting Spaces': int,
                    'Avg Number in Use': int,
                         'Max Number in Use': int
                   }

    df_meeting_spaces_used_floor = df_meeting_spaces_used_floor.astype(df_meeting_spaces_used_floor_columns_type).copy()
    df_meeting_spaces_used_floor = df_meeting_spaces_used_floor.drop('Hours in Use',axis=1)

    df_meeting_spaces_used_floor.fillna(value = 0,
              inplace = True)

    df_meeting_spaces_used_floor = df_meeting_spaces_used_floor.drop_duplicates()



    df_meeting_spaces_used_floor_b = {}
    df_meeting_spaces_used_floor_b_list = []

    #for every building sorting values by floor
    for building in building_names:
        df_meeting_spaces_used_floor_b[building] = df_meeting_spaces_used_floor.loc[df_meeting_spaces_used_floor['Building'] == building].copy()

        df_meeting_spaces_used_floor_b[building]['Floor2'] = df_meeting_spaces_used_floor_b[building]['Floor'].str.extract('(\d+)').astype(int)
        df_meeting_spaces_used_floor_b[building] = df_meeting_spaces_used_floor_b[building].sort_values(by = ['Floor2', 'Type'])

        df_meeting_spaces_used_floor_b[building]['Building']=df_meeting_spaces_used_floor_b[building]['Building'].mask(df_meeting_spaces_used_floor_b[building]['Building'].duplicated(),"")
        df_meeting_spaces_used_floor_b[building]['Floor']=df_meeting_spaces_used_floor_b[building]['Floor'].mask(df_meeting_spaces_used_floor_b[building]['Floor'].duplicated(),"")

        df_meeting_spaces_used_floor_b_list.append(df_meeting_spaces_used_floor_b[building])

        df_meeting_spaces_used_floor_final = pd.concat(df_meeting_spaces_used_floor_b_list)
        df_meeting_spaces_used_floor_final = df_meeting_spaces_used_floor_final.drop('Floor2',axis=1)


    return df_meeting_spaces_used_floor_final


@app.callback(
    Output('table-meeting-space-in-use', 'figure'),
    [
        Input('building-dropdown', 'value'),
        Input('floor-dropdown', 'value'),
        Input('department-dropdown', 'value'),
        Input('week', 'value'),
        Input('day', 'value'),
        Input('time', 'value')
    ]
)

def update_graph_meeting_space_in_use(building, floor, department, week, day, time):
    filtered_meeting_space_in_use = filter_meeting_spaces_in_use(dframe, building, floor, department, week, day, time)
    
    headerColor = 'white'
    rowEvenColor = 'white'
    rowOddColor = 'lightgrey'

    fig_meeting_spaces_used_floor_final = go.Table(
         columnwidth = [80,50,80,120,120,120],
        header=dict(values=list(['<b>Building<b>', '<b>Floor<b>', '<b>Type<b>', '<b>Number of Meeting Spaces<b>', '<b>Avg Number in Use<b>',
           '<b>Max Number in Use<b>']),
                    #line_width = 0.5,
                    fill_color=headerColor,
                    align=['left','left','left','right','right','right'],
                    font=dict(color='black', size=9)
                   ),
        cells=dict(values=[filtered_meeting_space_in_use['Building'],
                           filtered_meeting_space_in_use['Floor'],
                           filtered_meeting_space_in_use['Type'],
                           filtered_meeting_space_in_use['Number of Meeting Spaces'],
                           filtered_meeting_space_in_use['Avg Number in Use'],
                           filtered_meeting_space_in_use['Max Number in Use'],
                          ],
                   #line_width = 0.1,
                fill_color = [[rowOddColor,rowEvenColor]*len(filtered_meeting_space_in_use)],
                align = ['left','left','left','right','right','right'],
                font = dict(color = 'black', size = 9)
                  ))
    
    layout = go.Layout(title="Meeting Spaces in Use by Floor", title_x=0.1)
        
    return {
        'data': [fig_meeting_spaces_used_floor_final],
        'layout': layout
    }



if __name__ == '__main__':
    app.run_server(debug=True, port=9059)


# In[ ]:




