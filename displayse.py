from datetime import datetime
import random
import csv
import sqlite3
import pandas as pd
#from IPython.display import display
import chart_studio.plotly as py
import plotly.graph_objs as go
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import time
import os
from threading import Lock
import flask

lock = Lock()
option = []
PORT = 80
ADDRESS = '10.0.0.129'

server = flask.Flask(__name__)

app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server)

today = datetime.now().strftime('%d%m%Y') +  '0930'

today = datetime.strptime(today, '%d%m%Y%H%M')

conn = sqlite3.connect('artificialStock.db', check_same_thread=False)
c = conn.cursor()

lock.acquire(True)
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
name = [str(j[0]) for j in c.fetchall()]
lock.release()
for i in name:
    option.append({'label' : i , 'value' : i})

app.layout = html.Div(children=[
    html.Div([
        dcc.Dropdown(
            id='selector',
            options=option
        )
    ]),
    dcc.Markdown(
        id='pc',
        className='percentChange',
        children='-0.0%'
    ),
    dcc.Graph(
        id='Graph1'
        #animate=True
    ),
    dcc.Interval(
        id='graph-update',
        interval=1*1000
    )
])
@app.callback(Output('Graph1','figure'), [Input('graph-update', 'interval'), Input('selector', 'value')])
def update(i, value):
    if value == None:
        value = 'RuneArrows'
    lock.acquire(True)
    c.execute('SELECT close FROM ' + value + ' ORDER BY time DESC LIMIT 1;')
    listed = [int(j[0]) for j in c.fetchall()]
    runeArrowsdf = pd.read_sql_query("SELECT * FROM " + str(value), conn)
    lock.release()
    runeArrowsdf['time'] = pd.to_datetime(runeArrowsdf['time'], format='%d%m%Y%H%M')
    runeArrowsdata = [dict(type='candlestick',
                 x=runeArrowsdf['time'],
                 yaxis = 'y2',
                 open=runeArrowsdf['open'],
                 high=runeArrowsdf['high'],
                 low=runeArrowsdf['low'],
                 close=runeArrowsdf['close'])]
    runeArrowslayout = dict(title=str(value) + '<br>' + str(listed[0]) + ' GP', font=dict(color='#fff6e6'), xaxis=dict(rangeslider=dict(visible=False), range=[today, datetime.strptime(datetime.now().strftime('%d%m%Y%H%M'), '%d%m%Y%H%M')]) , paper_bgcolor='#1a1100',plot_bgcolor='#ffedcc')
    figure = {'data': runeArrowsdata, 'layout' : runeArrowslayout}
    return figure

@app.callback(Output('pc' ,'children'), [Input('graph-update', 'interval'), Input('selector', 'value')])
def percentUpdate(i, value):
    if value == None:
        value = 'RuneArrows'
    lock.acquire(True)
    c.execute('SELECT close FROM ' + value + ' ORDER BY time DESC LIMIT 1;')
    listed = [float(j[0]) for j in c.fetchall()]
    lock.release()
    lock.acquire(True)
    c.execute('SELECT close FROM ' + value + ' WHERE time = ' + '\'' + today.strftime('%d%m%Y%H%M') + '\';')
    open = [float(j[0]) for j in c.fetchall()]
    lock.release()
    result = format((((listed[0] - open[0]) / open[0]) * 100), '.2f')
    return str(result) + "%"
@app.callback(Output('pc' , 'style'), [Input('graph-update', 'interval'), Input('selector', 'value')])
def percentColor(i, value):
    if value == None:
        value = 'RuneArrows'
    lock.acquire(True)
    c.execute('SELECT close FROM ' + value + ' ORDER BY time DESC LIMIT 1;')
    listed = [float(j[0]) for j in c.fetchall()]
    lock.release()
    lock.acquire(True)
    c.execute('SELECT close FROM ' + value + ' WHERE time = ' + '\'' + today.strftime('%d%m%Y%H%M') + '\';')
    open = [float(j[0]) for j in c.fetchall()]
    lock.release()
    result = format((((listed[0] - open[0]) / open[0]) * 100), '.2f')
    if float(result) < 0.0:
        styleRed = {
                'z-index':'5',
                'color':'#CC342B',
                'position':'fixed',
                'left':'710px',
                'top':'76px',
                'font-size':'18.5px',
                'font-family':'Arial'
                }
        return styleRed
    if float(result) > 0.0:
        styleGreen = {
                'z-index':'5',
                'color':'#317A5A',
                'position':'fixed',
                'left':'710px',
                'top':'76px',
                'font-size':'18.5px',
                'font-family':'Arial'
                }
        return styleGreen

def app():
    app.run_server()
