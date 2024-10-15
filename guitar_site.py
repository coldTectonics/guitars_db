import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import re
import plotly.express as px
from dash import dash_table
import os
import sys


df = pd.read_csv('Guitars.csv',sep=';',decimal=',')

def restart():
    os.execv(sys.executable, ['python3'] + sys.argv)

app = dash.Dash(__name__)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.css.append_css({'external_url': '/static/reset.css'})
app.server.static_folder = 'static'
style = {'backgroundColor': '#111111','color': '#7FDBFF'}
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.title="Гитары на складе"

fig = px.bar(df, x="Товар", y="Количество", title="Гитары на складе")
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'margin-top':'30pt','backgroundColor': '#111111','color': '#7FDBFF', 'height': '100vh',"margin": "0px 0px 0px 0px"}, children=[
    html.Link(
        rel='stylesheet',
        href='/static/reset.css'
    ),
    html.Center ([
        html.H1(children='Гитары на складе'),

        dash_table.DataTable(
                id='editable-table',
                columns=[{"name": i, "id": i, "deletable": False, "renamable": False} for i in df.columns],
                data=df.to_dict('records'),
                editable=True, 
                row_deletable=True,  
                style_table={'width': '70%', 'margin': 'auto'},
                style_cell={'textAlign': 'center'},
                
                style_data = {'backgroundColor': '#111111','color': '#7FDBFF', 'border': '2px solid'},
                style_header = {'backgroundColor': '#111111','color': '#7FDBFF', 'border': '2px solid'}
        ),


        html.Button('Добавить строку', id='add-row-btn', n_clicks=0, style={'margin': '20px'}),
        html.Button('Сохранить в CSV', id='save-to-csv-btn', n_clicks=0, style={'margin': '20px'}),

        html.Div(id='success_message',children=''),
        dcc.Graph(
        id='example-graph-2',
        figure=fig,
        style={'margin-top':'30pt', 'width': '70vw'}
        ),
        html.Br(),
        html.Div('2022', style={'textAlign': 'center', 'color': '#7FDBFF'}),
        html.Div(id='status-msg', style={'margin-top': '20px'})

        ])  
    ])
@app.callback(
    Output('editable-table', 'data'),
    Input('add-row-btn', 'n_clicks'),
    State('editable-table', 'data'),
    State('editable-table', 'columns')
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output('status-msg', 'children'),
    Input('save-to-csv-btn', 'n_clicks'),
    State('editable-table', 'data')
)
def save_to_csv(n_clicks, rows):
    if n_clicks > 0:
        df_new = pd.DataFrame(rows)
        df_new.to_csv('Guitars.csv', index=False,sep=';',decimal=',')
        restart ()
        return 'Данные сохранены в CSV!'
    return ''

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
